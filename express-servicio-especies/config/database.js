const mysql = require('mysql2');
const dotenv = require('dotenv');

// Cargar variables del archivo .env
dotenv.config();

// Crear el pool de conexión usando variables de entorno
const pool = mysql.createPool({
  host: process.env.MYSQL_ADDON_HOST,
  port: process.env.MYSQL_ADDON_PORT || 3306,
  user: process.env.MYSQL_ADDON_USER,
  password: process.env.MYSQL_ADDON_PASSWORD,
  database: process.env.MYSQL_ADDON_DB
});

// Exportar el pool como promesa para usar async/await
module.exports = pool.promise();
