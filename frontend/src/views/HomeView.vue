<template>
  <div class="home-view">
    <!-- Título con estilo atractivo -->
    <h1 class="app-title">
      SongGenIA
    </h1>
    
    <!-- Imagen o GIF debajo del título -->
    <div class="image-container">
      <img
        src="@/assets/logo.jpg"
        alt="SongGenIA Logo"
        class="app-image"
      >
    </div>
    
    <!-- Sección de Login y Registro -->
    <div class="auth-links">
      <div class="auth-item">
        <router-link
          to="/login"
          class="auth-link"
        >
          Iniciar Sesión
        </router-link>
        <p>¿Ya tienes cuenta?</p>
      </div>
      <div class="auth-item">
        <router-link
          to="/register"
          class="auth-link"
        >
          Regístrate
        </router-link>
        <p>¿No tienes cuenta?</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
};
</script>

<style scoped>

.home-view {
  text-align: center;
  padding: 0;
  background: linear-gradient(to right, #6146b1, #7ec8e3);
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.app-title {
  font-size: 3rem;
  font-weight: bold;
  color: white; 
  margin-bottom: 20px;
}

.image-container {
  margin: 20px 0;
}

.app-image {
  width: 80%;
  max-width: 500px;
  height: auto;
}

.auth-links {
  margin-top: 30px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.auth-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.auth-link {
  color: #ffffff;
  text-decoration: none;
  border: 2px solid #ffffff;
  padding: 12px 35px;
  border-radius: 25px;
  background-color: rgba(71, 49, 131, 0.3); 
  font-size: 1.2rem;
  font-weight: bold;
  transition: all 0.3s ease;
}

.auth-link:hover {
  background-color: rgba(255, 255, 255, 0.6);
  color: #4a148c;
}
</style>