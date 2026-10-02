from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Ruta de la base de datos
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "house_analytics.db"


# Conectar con la base de datos
def conectar_db():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


# Página principal
@app.route("/")
def inicio():
    return jsonify({
        "mensaje": "API de House Analytics funcionando"
    })


# Obtener todas las viviendas
@app.route("/api/viviendas")
def viviendas():

    conexion = conectar_db()

    datos = conexion.execute(
        "SELECT * FROM viviendas"
    ).fetchall()

    conexion.close()

    viviendas = [
        dict(vivienda)
        for vivienda in datos
    ]

    return jsonify(viviendas)


# Obtener una vivienda específica
@app.route("/api/viviendas/<int:id>")
def vivienda(id):

    conexion = conectar_db()

    resultado = conexion.execute(
        "SELECT * FROM viviendas WHERE ID = ?",
        (id,)
    ).fetchone()

    conexion.close()

    if resultado is None:
        return jsonify({
            "error": "Vivienda no encontrada"
        }), 404

    return jsonify(dict(resultado))


# Ejecutar servidor
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=puerto,
        debug=False
    )