const { Sequelize, DataTypes } = require('sequelize');
const db = require('../config/db'); 

const User = db.define('User', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    nombre: {
        type: DataTypes.STRING,
        allowNull: false
    },
    cedula: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: true  
    },
    telefono: {
        type: DataTypes.STRING,
        allowNull: true  
    },
    email: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: false
    },
    password: {
        type: DataTypes.STRING,
        allowNull: true  
    },
    username: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: false
    }
}, {
    tableName: 'users',
    timestamps: false, 
});


User.sync().then(() => {
    console.log("Tabla 'users' creada o verificada.");
});

module.exports = User;
