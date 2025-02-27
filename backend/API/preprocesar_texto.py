import os
import json
import random
import numpy as np
import spacy
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from spacy_langdetect import LanguageDetector
from spacy.language import Language
from textblob import TextBlob


# ✅ 1. Obtener la ruta base
ruta_base = os.path.dirname(os.path.abspath(__file__))

# ✅ 2. Definir las rutas de los archivos
ruta_modelo = os.path.join(ruta_base, "..", "models", "modelo_nuevo2.keras")
ruta_tokenizador = os.path.join(ruta_base, "..", "models", "tokenizer.json")

# ✅ 3. Cargar el modelo
modelo = load_model(ruta_modelo)

# ✅ 4. Cargar el tokenizador desde JSON
if os.path.exists(ruta_tokenizador):
    with open(ruta_tokenizador, "r", encoding="utf-8") as f:
        token_json = f.read()
    tokenizador = tokenizer_from_json(token_json)
    print("✅ Tokenizador cargado correctamente.")
else:
    print("❌ ERROR: No se encontró 'tokenizer.json' en 'models/'. Verifica que lo hayas copiado correctamente.")
    exit()



def analizar_sentimiento(texto):
    """Analiza el sentimiento del texto del usuario y retorna una emoción general."""
    sentimiento = TextBlob(texto).sentiment.polarity  # Polarity entre -1 (negativo) y 1 (positivo)

    if sentimiento > 0.2:
        return "felicidad"
    elif sentimiento < -0.2:
        return "tristeza"
    else:
        return "neutralidad"
    

def generar_palabras_clave(texto_usuario):
    """Convierte la entrada del usuario en una idea abstracta para generar la letra."""
    emocion = analizar_sentimiento(texto_usuario)

    # Asociar palabras clave según la emoción detectada
    palabras_clave = {
        "felicidad": ["alegría", "brillo", "bailar", "luz", "amor"],
        "tristeza": ["lluvia", "soledad", "nostalgia", "sombra", "dolor"],
        "neutralidad": ["caminos", "espera", "sueños", "pensamiento", "mirada"]
    }
    
    return random.choice(palabras_clave[emocion])  # Elegir una palabra aleatoria

# ✅ 5. Cargar modelo de spaCy con detección de idioma
nlp = spacy.load("es_core_news_sm")
@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector()
nlp.add_pipe("language_detector", last=True)

def detectar_idioma(palabra):
    """Detecta si una palabra es español o no usando spaCy y un diccionario de palabras comunes."""
    doc = nlp(palabra)
    idioma_detectado = doc._.language["language"]

    # Lista de palabras en español más comunes para validar
    palabras_comunes_es = {"el", "la", "de", "en", "y", "con", "para", "por", "amor", "tristeza", "alegría", "camino"}

    # Si el modelo detecta español o si la palabra está en nuestro diccionario, la aceptamos
    return idioma_detectado == "es" or palabra.lower() in palabras_comunes_es


def preprocesar_texto(texto, max_length=15):
    """Convierte la entrada en tokens numéricos usando el tokenizador cargado."""
    tokens = texto.lower().split()
    secuencia = tokenizador.texts_to_sequences([tokens])
    secuencia_padded = pad_sequences(secuencia, maxlen=max_length, padding="post")
    return secuencia_padded

def nucleus_sampling(predictions, top_p=0.9):
    """Selecciona una palabra usando Top-p (Nucleus Sampling)."""
    sorted_indices = np.argsort(predictions)[::-1]  # Ordenar palabras de mayor a menor probabilidad
    sorted_probs = np.sort(predictions)[::-1]  # Ordenar probabilidades

    cumulative_probs = np.cumsum(sorted_probs)  # Calcular la suma acumulada de probabilidades
    top_p_index = np.where(cumulative_probs > top_p)[0][0]  # Obtener el punto de corte

    selected_indices = np.array(sorted_indices[:top_p_index + 1]).flatten()  # Asegurar que sea 1D

    if len(selected_indices) == 0:
        return np.argmax(predictions)  # Si no hay selección válida, usar la palabra más probable

    return np.random.choice(selected_indices)  # Elegir aleatoriamente una dentro del grupo


def contiene_signos_prohibidos(palabra):
    """Verifica si la palabra contiene signos que no queremos en la letra."""
    signos_prohibidos = set("¿¡!?;:")  # Lista de signos prohibidos
    return any(caracter in palabra for caracter in signos_prohibidos)

def generar_texto(texto_usuario, max_words=20, temperatura=0.5, top_p=0.9):
    """Genera una secuencia de texto basada en el sentimiento del usuario manteniendo coherencia con los tokens generados."""
    
    # Obtener una palabra inicial basada en la emoción detectada
    tema_generado = generar_palabras_clave(texto_usuario)
    texto_generado = [tema_generado]  # Primera palabra
    
    ultimas_palabras = set()
    palabras_generadas = 0

    while palabras_generadas < max_words:
        # Usar últimas 3-5 palabras como contexto para generar la siguiente palabra
        contexto = " ".join(texto_generado[-5:])  # Usamos las últimas palabras generadas
        entrada_procesada = preprocesar_texto(contexto)

        predicciones = modelo.predict(entrada_procesada, verbose=0)[0]
        predicciones = np.log(predicciones + 1e-8) / temperatura
        exp_preds = np.exp(predicciones)
        predicciones = exp_preds / np.sum(exp_preds)

        indice_palabra = nucleus_sampling(predicciones, top_p)
        palabra_generada = tokenizador.index_word.get(indice_palabra, None)

        # 🚨 Filtrar palabras fuera de contexto
        if not palabra_generada or palabra_generada in ultimas_palabras or not detectar_idioma(palabra_generada) or contiene_signos_prohibidos(palabra_generada):
            continue

        ultimas_palabras.add(palabra_generada)
        if len(ultimas_palabras) > 4:
            ultimas_palabras.pop()

        texto_generado.append(palabra_generada)
        palabras_generadas += 1

    # ✅ Aquí estructuramos los versos correctamente usando los tokens generados
    versos = []
    verso_actual = []

    for i, palabra in enumerate(texto_generado, start=1):
        verso_actual.append(palabra)

        if i % 4 == 0:  # Cada 4 palabras, crear un nuevo verso
            versos.append(" ".join(verso_actual))
            verso_actual = []

    if verso_actual:
        versos.append(" ".join(verso_actual))

    return "\n".join(versos)  # Devolver el texto con estructura de versos


# ✅ 7. Prueba del sistema
if __name__ == "__main__":
    entrada_usuario = input("🎶 Escribe una palabra o frase inicial: ")
    resultado = generar_texto(entrada_usuario)
    print(f"🎤 Texto generado: {resultado}")