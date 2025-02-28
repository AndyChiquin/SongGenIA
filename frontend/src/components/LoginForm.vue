<template>
  <div class="app-body">
    <div class="login-form">
      <h2 class="title">🔑 Iniciar sesión</h2>
      <form @submit.prevent="submitLogin">
        <div class="form-group">
          <label for="email" class="input-label">📧 Correo electrónico:</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Ingresa tu correo"
            required
          >
        </div>

        <div class="form-group">
          <label for="password" class="input-label">🔒 Contraseña:</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Ingresa tu contraseña"
            required
          >
        </div>

        <button type="submit" class="primary-button">
          Iniciar sesión
        </button>
      </form>

      <button @click="googleLogin" class="google-button">
        🟢 Iniciar sesión con Google
      </button>
      
      <router-link to="/" class="home-button">🏠 Volver a Inicio</router-link>

      <p
        v-if="errorMessage"
        class="error"
      >
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script>
import { login, loginWithGoogle } from "@/services/auth";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: null,
    };
  },
  mounted() {
    
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      localStorage.setItem("authToken", token);  
      this.$router.push("/dashboard");  
    }
  },
  methods: {
    async submitLogin() {
      try {
        const response = await login(this.email, this.password);

        if (response.token) {
          localStorage.setItem("authToken", response.token); 
          this.$router.push("/dashboard"); 
        } else {
          this.errorMessage = response.error || "Credenciales incorrectas.";
        }
      } catch (error) {
        this.errorMessage = "Error al iniciar sesión. Inténtalo de nuevo.";
      }
    },
    
    googleLogin() {
      loginWithGoogle(); 
    },
  }
};
</script>

<style scoped>

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


.login-form {
  max-width: 450px; 
  padding: 35px;
  border-radius: 12px;
  background: #f0f4ff;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25); 
  width: 100%; 
  text-align: center;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #3a3a3a;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.input-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c2c54;
}

input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #a8a8a8;
  background: #ffffff;
  transition: border 0.3s;
}

input:focus {
  border-color: #5a67d8;
  outline: none;
}

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

.google-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(to right, #f4b400, #db4437);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
  transition: background 0.3s, transform 0.2s;
}

.google-button:hover {
  background: linear-gradient(to right, #e2a000, #c1351d);
  transform: scale(1.05);
}

.home-button {
  display: inline-block;
  margin-top: 15px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: bold;
  color: #5a67d8;
  text-decoration: none;
  border: 2px solid #5a67d8;
  border-radius: 8px;
  transition: background 0.3s, color 0.3s;
}

.home-button:hover {
  background: #5a67d8;
  color: white;
}

button:focus {
  outline: none;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 15px;
  text-align: center;
}
</style>