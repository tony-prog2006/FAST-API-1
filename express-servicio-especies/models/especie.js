const db = require('../config/database');

const Especie = {
  getAll: async () => {
    const [rows] = await db.query('SELECT * FROM especies');
    return rows;
  }
};

module.exports = Especie;
