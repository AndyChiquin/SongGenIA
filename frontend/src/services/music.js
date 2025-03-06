import axios from "axios";
import { MUSIC_API_URL } from "./api"; // Importamos la URL base

// Función para generar la letra de la canción
export const generateLyrics = async (frase) => {
  try {
    const response = await axios.post(`${MUSIC_API_URL}/generar`, { 
      frase_inicial: frase
    });

    if (response.status === 200 && response.data.texto_generado) {
      return response.data.texto_generado;
    } else {
      console.error("Error: No se recibió la letra generada correctamente.");
      return null;
    }
  } catch (error) {
    console.error("Error al generar la letra:", error);
    return null;
  }
};

// Función para generar la música y obtener el Task ID
export const generateMusic = async (lyrics, genre, mood) => {
  try {
    const response = await axios.post(`${MUSIC_API_URL}/generate-music`, {
      lyrics,
      genre,
      mood,
    });

    console.log("Respuesta completa de la API al generar música:", response.data);

    if (response.status === 200 && response.data.data && response.data.data.taskId) {
      console.log("TaskId recibido:", response.data.data.taskId); 
      return response.data.data.taskId; 
    } else {
      console.error("Error: No se pudo iniciar la generación de la canción.");
      return null;
    }
  } catch (error) {
    console.error("Error al generar la música:", error);
    return null;
  }
};

// 🔹 Función mejorada para obtener la URL del audio de manera automática con reintentos
export const getAudio = async (taskId, maxAttempts = 10, interval = 5000) => {
  return new Promise((resolve) => {
    let attempts = 0;

    const checkAudio = async () => {
      try {
        console.log(`Intento ${attempts + 1}: Consultando el audio con Task ID: ${taskId}`);

        const response = await axios.get(`${MUSIC_API_URL}/get-audio/${taskId}`);
        console.log("Respuesta de la API al obtener el audio:", response.data);

        if (response.status === 200 && response.data.audio_links && response.data.audio_links.length > 0) {
          const audioUrl = response.data.audio_links[0].streamAudioUrl;
          console.log("✅ Audio URL obtenida:", audioUrl);
          resolve(audioUrl);
        } else if (attempts >= maxAttempts) {
          console.error("⛔ Se agotaron los intentos, no se encontró el audio.");
          resolve(null);
        } else {
          attempts++;
          setTimeout(checkAudio, interval);
        }
      } catch (error) {
        console.error("❌ Error al obtener el audio:", error);
        resolve(null);
      }
    };

    checkAudio();
  });
};
