# server.py
import os
from dotenv import load_dotenv
from Login_Register import create_app

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)