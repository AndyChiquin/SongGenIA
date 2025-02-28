# 🔹 Importar librerías necesarias  
import pandas as pd  
import numpy as np  
import nltk  
import re
import matplotlib.pyplot as plt  
from nltk.corpus import stopwords  
from wordcloud import WordCloud, STOPWORDS  
import gc  # Gestión de memoria
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout, BatchNormalization, TimeDistributed
from tensorflow.keras.callbacks import EarlyStopping


# Descargar stopwords en español si no están disponibles  
try:  
    nltk.data.find('corpora/stopwords')  
except LookupError:  
    nltk.download('stopwords')  

cachedStopWords = stopwords.words("spanish")  

# 📂 Cargar el dataset  
file_path = "archivo_filtrado.xlsx"  

try:  
    df = pd.read_excel(file_path, usecols=["artist", "lyrics", "title"])  
except ValueError as e:  
    print(f"Error al cargar el archivo: {e}")  
    exit()  

# Tomar solo el 70% de los datos para optimizar memoria  
df = df.sample(frac=0.7, random_state=42)  

# 🔍 Preprocesamiento de texto  
df["lyrics"] = df["lyrics"].fillna("").astype(str).str.lower().str.strip()  

# Tokenización de letras de canciones  
def song_to_token(text):  
    return text.replace('\n', '').split(' ')  

df["tokens"] = df["lyrics"].apply(song_to_token)  

# 📊 Estadísticas de longitud de las letras  
lyrics_list = [" ".join(tokens) for tokens in df["tokens"].tolist() if len(tokens) > 5]  
lyrics_length_list = [len(x.split(' ')) for x in lyrics_list]  

if lyrics_length_list:  
    print("\n📊 **Estadísticas de longitud de las canciones:**")  
    print(f"🔹 Longitud promedio: {round(np.mean(lyrics_length_list), 0)} palabras")  
    print(f"🔹 Longitud mínima: {np.min(lyrics_length_list)} palabras")  
    print(f"🔹 Longitud máxima: {np.max(lyrics_length_list)} palabras")  

# 🧠 **Preparación de datos**  
gc.collect()  # Liberar memoria  
vocab_size = 20000  
embedding_dim = 50  
max_length = 15  
batch_size = 64  

# 📌 **Tokenización y Padding**
tokenizer = Tokenizer(num_words=vocab_size)  
tokenizer.fit_on_texts(lyrics_list)  
sequences = tokenizer.texts_to_sequences(lyrics_list)  
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding="post")  

# 🔹 Guardar tokenizador  
tokenizer_json = tokenizer.to_json()  
with open("tokenizer.json", "w", encoding="utf-8") as f:  
    f.write(tokenizer_json)  

print("✅ Tokenizador guardado como 'tokenizer.json'.")  

# 🔥 **Generador de Datos para evitar problemas de memoria**
def data_generator(sequences, batch_size, vocab_size):
    while True:
        for i in range(0, len(sequences), batch_size):
            X_batch = sequences[i:i+batch_size, :-1]
            y_batch = sequences[i:i+batch_size, 1:]
            
            # Convertir dinámicamente a one-hot encoding
            y_batch = np.array([to_categorical(seq, num_classes=vocab_size) for seq in y_batch])
            
            yield X_batch, y_batch

# 📌 **Preparar Generador de Entrenamiento**
train_generator = data_generator(padded_sequences, batch_size, vocab_size)
steps_per_epoch = len(padded_sequences) // batch_size  

# 📌 **Modelo LSTM Mejorado**
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length-1),
    BatchNormalization(),
    Bidirectional(LSTM(128, return_sequences=True)),
    Dropout(0.2),
    LSTM(128, return_sequences=True),
    Dropout(0.2),
    LSTM(64, return_sequences=True),
    TimeDistributed(Dense(vocab_size, activation='softmax'))
])

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.summary()

# 🔥 **Configurar Early Stopping**
early_stopping = EarlyStopping(monitor='accuracy', patience=10, restore_best_weights=True, verbose=1)

# 📌 **Entrenamiento Usando Generator con Early Stopping**
model.fit(train_generator, 
          steps_per_epoch=steps_per_epoch, 
          epochs=200,  # El entrenamiento se detendrá automáticamente cuando ya no mejore
          verbose=1, 
          callbacks=[early_stopping])

# 💾 Guardar el modelo  
model.save("red5.keras")  
print("Modelo guardado correctamente.")  

# 🎶 **Generación de texto con rima y temperatura**  

# 🔹 Función para encontrar palabras con rimas en español
def get_rhyming_word_es(word, vocab_list):
    word = word.lower()
    last_syllable = re.findall(r'.{2,}$', word)  # Tomamos las últimas 2 o más letras
    if last_syllable:
        rhymes = [w for w in vocab_list if w.endswith(last_syllable[0]) and w != word]
        return np.random.choice(rhymes) if rhymes else word
    return word

# 🔹 Generación con control de temperatura
def generate_song_es(model, tokenizer, seed_text, max_length=15, next_words=50, temperature=1.0):
    output_text = seed_text
    vocab_list = list(tokenizer.index_word.values())  # Extraemos vocabulario del tokenizador

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([output_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_length-1, padding='pre')

        predicted_probs = model.predict(token_list, verbose=0)[0, -1, :]
        predicted_probs = np.log(predicted_probs + 1e-7) / temperature
        predicted_probs = np.exp(predicted_probs) / np.sum(np.exp(predicted_probs))

        predicted_index = np.random.choice(range(vocab_size), p=predicted_probs)

        word = tokenizer.index_word.get(int(predicted_index))
        if word is None or predicted_index == 0:
            break

        # Aplicar rima con 50% de probabilidad
        if np.random.rand() < 0.5:
            word = get_rhyming_word_es(word, vocab_list)

        output_text += ' ' + word

    return output_text

# 🎶 Generar una canción con una frase inicial
seed_text = "amor eterno"
generated_lyrics = generate_song_es(model, tokenizer, seed_text, next_words=50, temperature=0.8)

print("\n🎶 **Nueva canción generada en español con rima:**")
print(generated_lyrics)
