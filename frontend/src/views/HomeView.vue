<template>
  <div>
    <h1>🎵 SongGenIA</h1>
    <MusicForm />
    
    <!-- Sección de Login y Registro -->
    <div class="auth-links">
      <p>
        ¿Ya tienes cuenta? <router-link to="/login">
          Inicia sesión
        </router-link>
      </p>
      <p>
        ¿No tienes cuenta? <router-link to="/register">
          Regístrate
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>
import MusicForm from "@/components/MusicForm.vue";

export default {
  components: {
    MusicForm
  }
};
</script>

<style scoped>
.auth-links {
  margin-top: 20px;
  text-align: center;
}
.auth-links a {
  color: #007bff;
  text-decoration: none;
}
.auth-links a:hover {
  text-decoration: underline;
}
</style>
