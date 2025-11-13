const express = require('express');
const router = express.Router();
const consultaController = require('../controllers/consultaController');

// Ruta para obtener todas las especies
router.get('/especies', consultaController.getEspecies);

// Ruta para obtener condiciones por especie
router.get('/condiciones', consultaController.getCondiciones);

// Ruta para obtener zonas por especie
router.get('/zonas', consultaController.getZonas);

module.exports = router;
