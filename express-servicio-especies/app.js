const express = require('express');
const dotenv = require('dotenv');
const consultaRoutes = require('./routes/consultaRoutes');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Rutas del servicio
app.use('/api', consultaRoutes);

// Servidor activo
app.listen(PORT, () => {
  console.log(`Servidor Express corriendo en http://localhost:${PORT}`);
});
