from flask import Flask, request, jsonify
from flask_cors import CORS
from preprocesar_texto import generar_texto
from services.generate_music import generate_music, get_audio  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/generar', methods=['POST'])
def generar():
    """Recibe una frase inicial y genera texto basado en el modelo"""
    try:
        data = request.get_json()
        if not data or "frase_inicial" not in data:
            return jsonify({"error": "Debe incluir 'frase_inicial' en la solicitud"}), 400

        frase_inicial = data["frase_inicial"]
        texto_generado = generar_texto(frase_inicial)

        return jsonify({
            "frase_inicial": frase_inicial,
            "texto_generado": texto_generado
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@app.route('/generate-music', methods=['POST'])
def generate_music_api():
    """Recibe la letra generada y devuelve la URL de la canción generada"""
    try:
        data = request.get_json()
        if not data or "lyrics" not in data or "genre" not in data or "mood" not in data:
            return jsonify({"error": "Faltan datos en la solicitud"}), 400

        lyrics = data["lyrics"]
        genre = data["genre"]
        mood = data["mood"]

        result = generate_music(lyrics, genre, mood)  # Generamos la música usando la API configurada

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error en la generación de música: {str(e)}"}), 500

@app.route('/get-audio/<task_id>', methods=['GET'])
def get_audio_endpoint(task_id):
    """Retorna la URL del archivo de audio generado."""
    result = get_audio(task_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
