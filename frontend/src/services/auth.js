import axios from "axios";

const API_URL = "http://127.0.0.1:3000"; // Dirección del backend

// Iniciar sesión con correo y contraseña
export const login = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, { email, password });
    return response.data;
  } catch (error) {
    console.error("Error en el login:", error);
    return { error: error.response?.data?.message || "Error en la autenticación" };
  }
};

// Registrar un nuevo usuario
export const register = async (username, email, password) => {
  try {
    const response = await axios.post(`${API_URL}/register`, { username, email, password });
    return response.data;
  } catch (error) {
    console.error("Error en el registro:", error);
    return { error: error.response?.data?.message || "No se pudo registrar el usuario" };
  }
};

// Iniciar sesión con Google
export const loginWithGoogle = async () => {
  try {
    const response = await axios.get(`${API_URL}/auth/google`);
    window.location.href = response.data.auth_url; // Redirige a la autenticación de Google
  } catch (error) {
    console.error("Error en la autenticación con Google:", error);
  }
};
