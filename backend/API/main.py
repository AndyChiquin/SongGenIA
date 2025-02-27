from flask import Flask, request, jsonify
from services.generate_music import generar_cancion_con_suno, leer_letra_desde_archivo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Bienvenido a SongGenIA API"})

@app.route("/generate-music", methods=["POST"])
def generate_song():
    data = request.get_json()
    lyrics_file_path = "letra_generada.txt"  # Aquí está el archivo con la letra generada

    # Leer la letra desde el archivo
    try:
        letra = leer_letra_desde_archivo()
    except FileNotFoundError:
        return jsonify({"error": "El archivo de letra no se encuentra"}), 404

    genre = data.get("genre", "pop")  # Valor por defecto "pop" si no se pasa género
    mood = data.get("mood", "happy")  # Valor por defecto "happy" si no se pasa estado de ánimo

    if not letra or not genre or not mood:
        return jsonify({"error": "Faltan parámetros"}), 400

    # Generar música con la letra leída
    response = generar_cancion_con_suno(letra)
    return jsonify(response)

@app.route("/get-audio/<task_id>", methods=["GET"])
def check_audio(task_id):
    from services.generate_music import get_audio
    response = get_audio(task_id)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
