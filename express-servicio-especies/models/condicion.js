const db = require('../config/database');

const Condicion = {
  getByEspecieId: async (id_especie) => {
    const [rows] = await db.query(
      'SELECT * FROM condiciones WHERE id_especie = ?',
      [id_especie]
    );
    return rows;
  }
};

module.exports = Condicion;
