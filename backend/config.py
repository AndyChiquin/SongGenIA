import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()
API_KEY = os.getenv("SUNO_API_KEY")

print(f"API Key cargada: {API_KEY}")  # Verificar si la clave se está cargando correctamente
