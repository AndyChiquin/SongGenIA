import requests
from config import API_KEY

API_URL = "https://apibox.erweima.ai/api/v1/generate"
STATUS_URL = "https://apibox.erweima.ai/api/v1/generate/record-info"  # URL para consultar el estado de la tarea

def get_audio(task_id):
    """Consulta el estado de la generación de audio y extrae los enlaces."""
    url = f"{STATUS_URL}?taskId={task_id}"

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

def leer_letra_desde_archivo():
    """Lee la letra generada desde el archivo 'letra_generada.txt'."""
    try:
        with open("letra_generada.txt", "r", encoding="utf-8") as f:
            letra = f.read()
        return letra
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def generar_cancion_con_suno(letra, genre):
    """Genera música con la API de Suno AI usando la letra generada automáticamente."""
    url = API_URL  # Usamos la URL correcta de la API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Aquí estamos utilizando la letra leída desde el archivo
    data = {
        "text": letra,         # Aquí va la letra que leímos del archivo
        "style": genre,        # Estilo de la música (por ejemplo: "pop", "classical")
        "title": "Mi Canción", # Título de la música
        "customMode": True,    # Habilitar el modo personalizado
        "instrumental": False, # Si no quieres instrumental, ponlo en False
        "model": "V4",         # Usar la versión V4
        "duration": 30         # Duración en segundos
    }

    # Hacemos el POST a la API
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        resultado = response.json()
        task_id = resultado.get("task_id")
        print(f"🎵 Canción generada con task_id: {task_id}")

        # Ahora consulta el estado de la tarea con el task_id
        audio_info = get_audio(task_id)

        if "audio_links" in audio_info:
            for audio in audio_info["audio_links"]:
                print(f"🎶 Enlace de audio: {audio['streamAudioUrl']}")
        else:
            print("❌ Error al obtener el enlace de la canción:", audio_info.get("error"))
    else:
        print("❌ Error al generar la canción:", response.text)

# Probar con la letra generada desde el archivo
if __name__ == "__main__":
    letra_generada = leer_letra_desde_archivo()
    if letra_generada:
        print(f"🎤 Texto generado: {letra_generada}")
        generar_cancion_con_suno(letra_generada, "Pop")  # Puedes cambiar el estilo aquí
    else:
        print("❌ No se pudo leer la letra generada.")
