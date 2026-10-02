from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


# Conectar con la base de datos
def conectar_db():
    conexion = sqlite3.connect("house_analytics.db")
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
    app.run(
        debug=True,
        port=5000
    )