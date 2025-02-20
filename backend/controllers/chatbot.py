import time
from services.generate_music import generate_music, get_audio

def chatbot():
    print("🎵 ¡Bienvenido a SongGenIA - Generador de Canciones con IA! 🎵")
    while True:
        frase = input("\n📝 Escribe una frase para tu canción (o escribe 'salir' para terminar): ")
        if frase.lower() == "salir":
            print("👋 ¡Hasta la próxima!")
            break
        
        genero = input("🎼 ¿Qué género musical quieres? (Ej: Pasillo, Sanjuanito, Albazo): ")
        sentimiento = input("😊 ¿Qué emoción quieres transmitir? (Ej: alegre, triste, romántico): ")

        print("\n🎶 Generando tu canción, por favor espera...")
        resultado = generate_music(frase, genero, sentimiento)

        if resultado and "data" in resultado:
            task_id = resultado["data"].get("taskId")
            print(f"\n✅ Canción en proceso. ID de tarea: {task_id}")
            
            print("⌛ Esperando la canción...")

            # 📌 Esperar hasta que la canción esté lista
            max_retries = 10  # Número máximo de intentos
            wait_time = 5  # Segundos entre intentos

            for _ in range(max_retries):
                audio_result = get_audio(task_id)
                status = audio_result.get("data", {}).get("status", "")

                if status == "SUCCESS":
                    print("\n🎧 ¡Aquí tienes tu canción!")
                    for i, audio in enumerate(audio_result["data"]["response"]["sunoData"], 1):
                        print(f"{i}. 🔊 {audio['streamAudioUrl']}")
                    break
                else:
                    print("⌛ La canción aún se está procesando... Esperando 5 segundos.")
                    time.sleep(wait_time)
            else:
                print("❌ La canción no está lista después de varios intentos. Intenta más tarde.")
        else:
            print("❌ Hubo un error al generar la canción. Intenta de nuevo.")

if __name__ == "__main__":
    chatbot()
