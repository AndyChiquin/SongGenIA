module.exports = {
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/api/auth": {
        target: "http://localhost:3000",
        changeOrigin: true
      },
      "/api/music": {
        target: "http://localhost:5000",
        changeOrigin: true
      }
    }
  }
};
