const db = require('../config/database');

const Zona = {
  getByEspecieId: async (id_especie) => {
    const [rows] = await db.query(
      'SELECT * FROM zonas WHERE id_especie = ?',
      [id_especie]
    );
    return rows;
  }
};

module.exports = Zona;
