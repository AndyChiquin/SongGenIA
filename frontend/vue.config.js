module.exports = {
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/api/auth": {
        target: "http://localhost:3000",  // Asegúrate de que el backend esté en este puerto
        changeOrigin: true
      },
      "/api/music": {
        target: "http://localhost:5000",  // Si estás usando otro backend para música
        changeOrigin: true
      }
    }
  }
};
