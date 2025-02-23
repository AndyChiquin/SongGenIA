import axios from "axios";
import { AUTH_API_URL } from "./api"; 

export const login = async (email, password) => {
  try {
    const response = await axios.post(`${AUTH_API_URL}/login`, { email, password });
    return response.data;
  } catch (error) {
    console.error("Error en el login:", error);
    return { error: error.response?.data?.message || "Error en la autenticación" };
  }
};

export const register = async (username, email, password) => {
  try {
    const response = await axios.post(`${AUTH_API_URL}/register`, { username, email, password });
    return response.data;
  } catch (error) {
    console.error("Error en el registro:", error);
    return { error: error.response?.data?.message || "No se pudo registrar el usuario" };
  }
};

export const loginWithGoogle = async () => {
  try {
    const response = await axios.get(`${AUTH_API_URL}/auth/google`);
    window.location.href = response.data.auth_url; // Redirige a la autenticación de Google
  } catch (error) {
    console.error("Error en la autenticación con Google:", error);
  }
};
