<template>
  <div class="register-container">
    <h2>Registro de Usuario</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="nombre">Nombre</label>
        <input
          id="nombre"
          v-model="user.nombre"
          type="text"
          required
        >
      </div>
      <div class="form-group">
        <label for="cedula">Cédula</label>
        <input
          id="cedula"
          v-model="user.cedula"
          type="text"
          required
        >
      </div>
      <div class="form-group">
        <label for="telefono">Teléfono</label>
        <input
          id="telefono"
          v-model="user.telefono"
          type="text"
          required
        >
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="user.email"
          type="email"
          required
        >
      </div>
      <div class="form-group">
        <label for="username">Usuario</label>
        <input
          id="username"
          v-model="user.username"
          type="text"
          required
        >
      </div>
      <div class="form-group">
        <label for="password">Contraseña</label>
        <input
          id="password"
          v-model="user.password"
          type="password"
          required
        >
      </div>
      <button type="submit">
        Registrar
      </button>
      <p
        v-if="error"
        class="error"
      >
        {{ error }}
      </p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      user: {
        nombre: "",
        cedula: "",
        telefono: "",
        email: "",
        username: "",
        password: ""
      },
      error: null
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post("http://localhost:5000/register", this.user);
        alert(response.data.msg);
        this.$router.push("/login");
      } catch (error) {
        this.error = error.response?.data?.msg || "Error al registrar el usuario";
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background: #f9f9f9;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  font-weight: bold;
}
input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background: #0056b3;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
