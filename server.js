const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const passport = require('passport');
const session = require('express-session');
const authRoutes = require('./backend/login/routes/auth');
const sequelize = require('./backend/login/config/db');
const path = require('path');

dotenv.config();

const app = express();
app.use(express.json());
app.use(cors());

app.use(session({ secret: process.env.SECRET_KEY, resave: false, saveUninitialized: false }));
app.use(passport.initialize());
app.use(passport.session());

// Sirve los archivos estáticos (CSS, JS, imágenes) desde la carpeta frontend/assets
app.use(express.static(path.join(__dirname, 'frontend')));

// Rutas para los archivos HTML en frontend/views
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'views', 'login.html'));
});

app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'views', 'register.html'));
});

app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'views', 'dashboard.html'));
});

// Rutas de autenticación
app.use('/login/auth', authRoutes);

// Conexión con la base de datos
sequelize.sync()
  .then(() => console.log('Base de datos sincronizada con Sequelize'))
  .catch(err => console.error('Error al sincronizar la base de datos:', err));

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Corriendo en el puerto ${PORT}`);
});
