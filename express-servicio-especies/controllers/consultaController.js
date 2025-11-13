const Especie = require('../models/especie');
const Condicion = require('../models/condicion');
const Zona = require('../models/zona');

const consultaController = {
  // GET /api/especies
  getEspecies: async (req, res) => {
    try {
      const especies = await Especie.getAll();
      res.json(especies);
    } catch (error) {
      res.status(500).json({ error: 'Error al obtener especies' });
    }
  },

  // GET /api/condiciones?especie_id=1
  getCondiciones: async (req, res) => {
    const { especie_id } = req.query;
    try {
      const condiciones = await Condicion.getByEspecieId(especie_id);
      res.json(condiciones);
    } catch (error) {
      res.status(500).json({ error: 'Error al obtener condiciones' });
    }
  },

  // GET /api/zonas?especie_id=1
  getZonas: async (req, res) => {
    const { especie_id } = req.query;
    try {
      const zonas = await Zona.getByEspecieId(especie_id);
      res.json(zonas);
    } catch (error) {
      res.status(500).json({ error: 'Error al obtener zonas' });
    }
  }
};

module.exports = consultaController;
