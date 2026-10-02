from flask import Flask, jsonify, request
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


# Crear tabla de usuarios
def crear_tabla_usuarios():
    conexion = conectar_db()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            rol TEXT NOT NULL,
            password TEXT
        )
    """)

    conexion.execute("""
        INSERT OR IGNORE INTO usuarios
        (id, nombre, correo, rol, password)
        VALUES
        (1, 'Administrador', 'admin@houseanalytics.com',
        'administrador', 'admin123')
    """)

    conexion.execute("""
        INSERT OR IGNORE INTO usuarios
        (id, nombre, correo, rol, password)
        VALUES
        (2, 'Usuario Demo', 'usuario@houseanalytics.com',
        'usuario', 'usuario123')
    """)

    conexion.commit()
    conexion.close()


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


# Inicio de sesión
@app.route("/login", methods=["POST"])
def login():

    datos = request.get_json()

    if not datos:
        return jsonify({
            "error": "No se recibieron datos"
        }), 400

    correo = datos.get("correo")
    password = datos.get("password")

    if not correo or not password:
        return jsonify({
            "error": "Correo y contraseña son obligatorios"
        }), 400

    conexion = conectar_db()

    usuario = conexion.execute(
        """
        SELECT id, nombre, correo, rol
        FROM usuarios
        WHERE correo = ? AND password = ?
        """,
        (correo, password)
    ).fetchone()

    conexion.close()

    if usuario is None:
        return jsonify({
            "error": "Correo o contraseña incorrectos"
        }), 401

    return jsonify({
        "mensaje": "Inicio de sesión correcto",
        "usuario": dict(usuario)
    })


# Ejecutar servidor
if __name__ == "__main__":

    crear_tabla_usuarios()

    puerto = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=puerto,
        debug=False
    )