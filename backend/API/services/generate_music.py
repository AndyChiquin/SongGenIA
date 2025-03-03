import requests
import time
import os
from dotenv import load_dotenv  # Importa dotenv para cargar variables de entorno

# Cargar variables de entorno desde el archivo .env
load_dotenv()

API_KEY = os.getenv("SUNO_API_KEY")  # Obtener la clave API desde el .env

API_URL = "https://apibox.erweima.ai/api/v1/generate"
CALLBACK_URL = "https://webhook.site/tu-url-de-prueba"  # Puedes cambiar esto si es necesario
LETRA_ARCHIVO = r"C:\Users\Pc\Documents\GitHub\SongGenIA\backend\API\letra_generada.txt"

def cargar_letra_desde_archivo():
    """Carga la letra de la canción desde un archivo de texto."""
    try:
        with open(LETRA_ARCHIVO, "r", encoding="utf-8", errors="ignore") as file:
            letra = file.read().strip()
        return letra
    except FileNotFoundError:
        return None

def get_audio(task_id):
    """Consulta el estado de la generación de audio y extrae los enlaces."""
    url = f"https://apibox.erweima.ai/api/v1/generate/record-info?taskId={task_id}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        print("Estado de la tarea:", response.status_code, response.text)

        if response.status_code == 200:
            data = response.json()
            print("Datos completos de la respuesta:", data)

            if not data or "data" not in data:
                return {"error": "La API no devolvió datos válidos."}

            suno_data = data.get("data", {}).get("response", {}).get("sunoData", [])

            if not suno_data:
                return {"taskId": task_id, "status": "PENDING", "message": "La canción aún está procesándose."}

            audio_links = [
                {
                    "streamAudioUrl": song.get("streamAudioUrl"),
                    "sourceStreamAudioUrl": song.get("sourceStreamAudioUrl")
                } for song in suno_data
            ]

            return {"taskId": task_id, "audio_links": audio_links}
        else:
            return {"error": f"Error en la API: {response.text}"}
    except Exception as e:
        return {"error": f"Excepción en la solicitud: {str(e)}"}

def generate_music(lyrics=None, genre="Pasillo", mood="Alegre", instrumental=False):
    """Genera música con la API de Suno AI usando la letra proporcionada o desde un archivo."""
    if not API_KEY:
        return {"error": "No se encontró la clave API."}

    if not lyrics:
        print("⚠️ No se recibió letra desde la API, cargando desde el archivo...")
        lyrics = cargar_letra_desde_archivo()

    if not lyrics:
        return {"error": "No se encontró la letra de la canción ni en la API ni en el archivo."}

    payload = {
        "prompt": lyrics,
        "style": genre,
        "mood": mood,
        "title": "Canción generada",
        "customMode": True,
        "instrumental": instrumental,
        "model": "V3_5",
        "callBackUrl": CALLBACK_URL
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        print("Respuesta de Suno AI:", response.status_code, response.text)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}
