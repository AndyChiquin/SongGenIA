const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/user');


exports.register = async (req, res) => {
    const { nombre, cedula, telefono, email, password, username } = req.body;

    if (!nombre || !cedula || !telefono || !email || !password || !username) {
        return res.status(400).json({ msg: "Todos los campos son obligatorios" });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    try {
        const user = await User.create({
            nombre,
            cedula,
            telefono,
            email,
            password: hashedPassword,
            username
        });
        res.status(201).json({ msg: "Usuario registrado correctamente" });
    } catch (error) {
        res.status(500).json({ msg: "Error al registrar el usuario", error: error.message });
    }
};


exports.login = async (req, res) => {
    const { email, password } = req.body;
    const user = await User.findOne({ where: { email } });

    if (!user || !(await bcrypt.compare(password, user.password))) {
        return res.status(401).json({ msg: "Credenciales inválidas" });
    }

    const token = jwt.sign({ id: user.id, email: user.email }, process.env.SECRET_KEY, { expiresIn: process.env.ACCESS_TOKEN_EXPIRATION });
    res.json({ token, user });
};
