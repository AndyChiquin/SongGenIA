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

// Función para generar la música
export const generateMusic = async (lyrics, genre, mood) => {
  try {
    const response = await axios.post(`${MUSIC_API_URL}/generate-music`, {
      lyrics,
      genre,
      mood,
    });

    console.log("Respuesta completa de la API al generar música:", response.data); // Debugging

    if (response.status === 200 && response.data.taskId) {
      return response.data.taskId; // Se asegura de devolver solo el ID
    } else {
      console.error("Error: No se pudo iniciar la generación de la canción.");
      return null;
    }
  } catch (error) {
    console.error("Error al generar la música:", error);
    return null;
  }
};

// Función para obtener el audio generado usando el Task ID
export const getAudio = async (taskId) => {
  try {
    console.log(`Consultando el audio con Task ID: ${taskId}`); // Debugging

    const response = await axios.get(`${MUSIC_API_URL}/get-audio/${taskId}`);

    if (response.status === 200 && response.data.audio_links) {
      console.log("Respuesta de getAudio:", response.data); // Debugging
      return response.data.audio_links[0].streamAudioUrl; // Retorna solo la URL del audio
    } else {
      console.error("Error: No se encontró el audio generado.");
      return null;
    }
  } catch (error) {
    console.error("Error al obtener el audio:", error);
    return null;
  }
};
