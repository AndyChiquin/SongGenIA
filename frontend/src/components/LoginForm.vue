<template>
  <div class="login-form">
    <h2>🔑 Iniciar sesión</h2>
    <form @submit.prevent="submitLogin">
      <label for="email">📧 Correo electrónico:</label>
      <input
        id="email"
        v-model="email"
        type="email"
        placeholder="Ingresa tu correo"
        required
      >

      <label for="password">🔒 Contraseña:</label>
      <input
        id="password"
        v-model="password"
        type="password"
        placeholder="Ingresa tu contraseña"
        required
      >

      <button type="submit">
        Iniciar sesión
      </button>
    </form>

    <button @click="googleLogin">
      🟢 Iniciar sesión con Google
    </button>

    <p
      v-if="errorMessage"
      class="error"
    >
      {{ errorMessage }}
    </p>
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
  methods: {
    async submitLogin() {
      try {
        const response = await login(this.email, this.password);

        if (response.token) {
          localStorage.setItem("authToken", response.token); // Guardamos el token
          this.$router.push("/dashboard"); // Redirigir al dashboard
        } else {
          this.errorMessage = response.error || "Credenciales incorrectas.";
        }
      } catch (error) {
        this.errorMessage = "Error al iniciar sesión. Inténtalo de nuevo.";
      }
    },
    googleLogin() {
      loginWithGoogle();
    }
  }
};
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.error {
  color: red;
}
</style>
