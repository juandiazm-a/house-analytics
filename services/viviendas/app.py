from flask import Flask, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

# Ruta de la base de datos
BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE = BASE_DIR / "backend" / "house_analytics.db"


def conectar_db():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


# Comprobar que el microservicio funciona
@app.route("/")
def inicio():
    return jsonify({
        "servicio": "Microservicio de Viviendas",
        "estado": "funcionando"
    })


# Obtener todas las viviendas
@app.route("/viviendas")
def viviendas():

    conexion = conectar_db()

    datos = conexion.execute(
        "SELECT * FROM viviendas"
    ).fetchall()

    conexion.close()

    resultado = [
        dict(vivienda)
        for vivienda in datos
    ]

    return jsonify(resultado)


# Obtener una vivienda por ID
@app.route("/viviendas/<int:id>")
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


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001
    )