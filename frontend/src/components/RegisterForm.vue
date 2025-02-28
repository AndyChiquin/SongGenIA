<template>
  <div class="app-body">
    <div class="register-container">
      <h2 class="title">🆕 Registro de Usuario</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="nombre">Nombre</label>
          <input id="nombre" v-model="user.nombre" type="text" required>
        </div>
        <div class="form-group">
          <label for="cedula">Cédula</label>
          <input id="cedula" v-model="user.cedula" type="text" required>
        </div>
        <div class="form-group">
          <label for="telefono">Teléfono</label>
          <input id="telefono" v-model="user.telefono" type="text" required>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="user.email" type="email" required>
        </div>
        <div class="form-group">
          <label for="username">Usuario</label>
          <input id="username" v-model="user.username" type="text" required>
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input id="password" v-model="user.password" type="password" required>
        </div>
        <button type="submit" class="primary-button">Registrar</button>
        <router-link to="/" class="home-button">🏠 Volver a Inicio</router-link>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
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
        const response = await axios.post("http://localhost:3000/register", this.user);
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


.register-container {
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


label {
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


.error {
  color: red;
  font-size: 14px;
  margin-top: 15px;
  text-align: center;
}
</style>
