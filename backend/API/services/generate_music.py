import requests
from config import API_KEY

API_URL = "https://apibox.erweima.ai/api/v1/generate"
CALLBACK_URL = "https://webhook.site/tu-url-de-prueba"  # Cambia esto a tu URL real

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

            if not data or "data" not in data:
                return {"error": "La API no devolvió datos válidos."}

            suno_data = data.get("data", {}).get("response", {}).get("sunoData", [])

            # Si no hay datos en sunoData, significa que la canción aún no está lista
            if not suno_data:
                return {"taskId": task_id, "status": "PENDING", "message": "La canción aún está procesándose."}

            # Extraer los enlaces de los audios generados
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

def generate_music(lyrics, genre, mood, instrumental=False):
    """Genera música con la API de Suno AI."""
    if not API_KEY:
        return {"error": "No se encontró la clave API."}

    payload = {
        "prompt": lyrics,  # Frase del usuario
        "style": genre,  # Género musical
        "title": "Canción generada",  # Nombre de la canción
        "customMode": True,  # Modo personalizado obligatorio
        "instrumental": instrumental,  # False para voz, True para instrumental
        "model": "V3_5",  # Versión del modelo (ajusta si es necesario)
        "callBackUrl": CALLBACK_URL  # URL de callback
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
