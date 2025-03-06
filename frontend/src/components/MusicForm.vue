<template>
  <div class="app-body">
    <div class="music-form">
      <h2 class="title">🎶 Genera tu Canción con IA</h2>

      <!-- Entrada de frase inicial -->
      <div class="form-group">
        <label class="input-label">📝 Escribe una frase:</label>
        <input v-model="fraseInicial" type="text" placeholder="Escribe aquí..." required>
      </div>

      <!-- Botón para generar la letra -->
      <button @click="generarLetra" class="primary-button">
        ✍️ Generar Letra
      </button>

      <!-- Mensaje de carga -->
      <p v-if="loading" class="loading-text">⌛ Procesando...</p>

      <!-- Recuadro donde se muestra la letra generada -->
      <div class="lyrics-box">
        <h3>🎵 Letra Generada:</h3>
        <textarea v-model="lyrics" readonly class="lyrics-textarea"></textarea>
      </div>

      <!-- Opciones de género y estado de ánimo -->
      <div class="form-group">
        <label class="input-label">🎼 Género:</label>
        <select v-model="genre">
          <option>Bachata</option>
          <option>Rock</option>
          <option>Pop</option>
        </select>
      </div>

      <div class="form-group">
        <label class="input-label">😊 Estado de ánimo:</label>
        <select v-model="mood">
          <option>Alegre</option>
          <option>Triste</option>
          <option>Romántico</option>
        </select>
      </div>

      <!-- Botón para generar la música -->
      <button @click="generarMusica" class="primary-button">
        🎤 Generar Canción
      </button>

      <!-- Mensaje de espera -->
      <p v-if="waitingForAudio">🎵 Esperando la canción... Esto puede tardar unos segundos.</p>

      <!-- Mostrar la URL cuando la música se genere -->
      <div class="lyrics-box">
        <h3>📢 Tu canción está lista 🎶</h3>
        <input v-model="audioUrl" readonly class="lyrics-textarea">
        <a v-if="audioUrl" :href="audioUrl" target="_blank" class="primary-button">🔗 Ir a la Canción</a>
      </div>
    </div>
  </div>
</template>

<script>
import { generateLyrics, generateMusic, getAudio } from "@/services/music";

export default {
  data() {
    return {
      fraseInicial: "", // Texto ingresado por el usuario
      lyrics: "", // Letra generada
      genre: "Pasillo",
      mood: "Alegre",
      loading: false,
      taskId: "", // Aquí guardamos el Task ID
      audioUrl: "", // Aquí guardamos la URL del audio
      waitingForAudio: false // Indicador de espera para la URL
    };
  },
  methods: {
    async generarLetra() {
      if (!this.fraseInicial) {
        alert("Por favor, ingresa una frase inicial.");
        return;
      }

      this.loading = true;
      const letra = await generateLyrics(this.fraseInicial);

      if (letra) {
        this.lyrics = letra; 
      } else {
        alert("Error al generar la letra.");
      }

      this.loading = false;
    },

    async generarMusica() {
      if (!this.lyrics) {
        alert("Primero genera la letra.");
        return;
      }

      this.loading = true;
      this.waitingForAudio = true;

      const taskId = await generateMusic(this.lyrics, this.genre, this.mood);

      if (taskId) {
        this.taskId = taskId;  
        console.log("Task ID recibido:", this.taskId);

        this.audioUrl = await getAudio(this.taskId); // Espera hasta obtener la URL
        if (!this.audioUrl) {
          alert("No se pudo obtener la URL del audio.");
        }
      } else {
        alert("Error al generar la música.");
      }

      this.loading = false;
      this.waitingForAudio = false;
    }
  }
};
</script>





<style scoped>
/* Fondo global */
.app-body {
  background: linear-gradient(to right, #6146b1, #7ec8e3);
  font-family: 'Poppins', sans-serif;
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
}

/* Contenedor del formulario */
.music-form {
  max-width: 420px;
  padding: 30px;
  border-radius: 12px;
  background: #f0f4ff;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  width: 100%;
  text-align: center;
}

/* Títulos */
.title, h3 {
  font-size: 20px;
  font-weight: bold;
  color: #3a3a3a;
  margin-bottom: 10px;
}

/* Campos de entrada */
input, select {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #a8a8a8;
  background: #ffffff;
}

.lyrics-textarea {
  width: 100%;
  height: 50px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 8px;
  font-size: 14px;
  background: #fff;
}

/* Botón principal */
.primary-button {
  width: 100%;
  padding: 10px;
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.primary-button:hover {
  background: linear-gradient(to right, #580d99, #1e5bbf);
}

/* Botón secundario */
.secondary-button {
  width: 100%;
  padding: 10px;
  background: linear-gradient(to right, #ff7f50, #ff4500);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.secondary-button:hover {
  background: linear-gradient(to right, #ff6347, #ff2200);
}
</style>
