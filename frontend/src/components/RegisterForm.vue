<template>
  <div class="register-form">
    <h2>📝 Crear cuenta</h2>
    <form @submit.prevent="submitRegister">
      <label for="username">👤 Nombre de usuario:</label>
      <input v-model="username" type="text" id="username" placeholder="Ingresa tu nombre" required />

      <label for="email">📧 Correo electrónico:</label>
      <input v-model="email" type="email" id="email" placeholder="Ingresa tu correo" required />

      <label for="password">🔒 Contraseña:</label>
      <input v-model="password" type="password" id="password" placeholder="Ingresa tu contraseña" required />

      <button type="submit">Crear cuenta</button>
    </form>

    <button @click="submitGoogleRegister">🟢 Registrarse con Google</button>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { register, loginWithGoogle } from "@/services/auth"; // Importamos desde `auth.js`

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      errorMessage: null,
    };
  },
  methods: {
    async submitRegister() {
      try {
        const response = await register(this.username, this.email, this.password);
        if (response.error) {
          this.errorMessage = response.error;
        } else {
          this.$router.push("/login"); // Redirigir al login después del registro exitoso
        }
      } catch (error) {
        this.errorMessage = "Hubo un error al crear la cuenta.";
      }
    },
    submitGoogleRegister() {
      loginWithGoogle(); // Llama a la autenticación con Google
    }
  }
};
</script>

<style scoped>
.register-form {
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
