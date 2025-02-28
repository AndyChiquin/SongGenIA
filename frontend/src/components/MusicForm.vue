<template>
  <div class="app-body">
    <div class="music-form">
      <h2 class="title">🎶 Genera tu Canción con IA</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label class="input-label">📝 Escribe una frase:</label>
          <input
            v-model="lyrics"
            type="text"
            placeholder="Escribe aquí..."
            required
          >
        </div>

        <div class="form-group">
          <label class="input-label">🎼 Género:</label>
          <select v-model="genre">
            <option>Pasillo</option>
            <option>Sanjuanito</option>
            <option>Albazo</option>
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

        <button type="submit" class="primary-button">
          🎤 Generar Canción
        </button>
      </form>

      <p v-if="loading" class="loading-text">
        ⌛ Generando canción...
      </p>
      <p v-if="taskId" class="task-id">
        ✅ ID de tarea: {{ taskId }}
      </p>
    </div>
  </div>
</template>

<script>
import { generateMusic } from "@/services/music";

export default {
  data() {
    return {
      lyrics: "",
      genre: "Pasillo",
      mood: "Alegre",
      taskId: null,
      loading: false
    };
  },
  methods: {
    async submitForm() {
      this.loading = true;
      const response = await generateMusic(this.lyrics, this.genre, this.mood);
      if (response.data) {
        this.taskId = response.data.taskId;
      } else {
        alert("Error al generar la canción");
      }
      this.loading = false;
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

/* Título */
.title {
  font-size: 24px;
  font-weight: bold;
  color: #3a3a3a;
  margin-bottom: 20px;
}

/* Estilo de los grupos de formulario */
.form-group {
  margin-bottom: 15px;
  text-align: left;
}

/* Estilo de las etiquetas */
.input-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c2c54;
}

/* Campos de entrada */
input, select {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #a8a8a8;
  background: #ffffff;
  transition: border 0.3s;
}

input:focus, select:focus {
  border-color: #5a67d8;
  outline: none;
}

/* Botón principal */
.primary-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 15px;
  transition: background 0.3s, transform 0.2s;
}

.primary-button:hover {
  background: linear-gradient(to right, #580d99, #1e5bbf);
  transform: scale(1.05);
}

/* Texto de carga */
.loading-text {
  font-size: 14px;
  color: #ff9800;
  margin-top: 15px;
}

/* ID de la tarea generada */
.task-id {
  font-size: 14px;
  color: #2d9c5b;
  font-weight: bold;
  margin-top: 10px;
}
</style>
