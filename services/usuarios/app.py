from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE = BASE_DIR / "backend" / "house_analytics.db"


# Permitir conexiones desde el frontend
@app.after_request
def agregar_cors(respuesta):
    respuesta.headers["Access-Control-Allow-Origin"] = "*"
    respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    respuesta.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return respuesta


def conectar_db():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla():
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

    columnas = conexion.execute(
        "PRAGMA table_info(usuarios)"
    ).fetchall()

    nombres_columnas = [
        columna["name"]
        for columna in columnas
    ]

    if "password" not in nombres_columnas:
        conexion.execute(
            "ALTER TABLE usuarios ADD COLUMN password TEXT"
        )

    conexion.execute("""
        INSERT OR IGNORE INTO usuarios
        (id, nombre, correo, rol, password)
        VALUES
        (
            1,
            'Administrador',
            'admin@houseanalytics.com',
            'administrador',
            'admin123'
        )
    """)

    conexion.execute("""
        INSERT OR IGNORE INTO usuarios
        (id, nombre, correo, rol, password)
        VALUES
        (
            2,
            'Usuario Demo',
            'usuario@houseanalytics.com',
            'usuario',
            'usuario123'
        )
    """)

    conexion.execute("""
        UPDATE usuarios
        SET password = 'admin123'
        WHERE correo = 'admin@houseanalytics.com'
    """)

    conexion.execute("""
        UPDATE usuarios
        SET password = 'usuario123'
        WHERE correo = 'usuario@houseanalytics.com'
    """)

    conexion.commit()
    conexion.close()


@app.route("/")
def inicio():
    return jsonify({
        "servicio": "Microservicio de Usuarios",
        "estado": "funcionando"
    })


@app.route("/usuarios")
def usuarios():
    conexion = conectar_db()

    datos = conexion.execute(
        "SELECT id, nombre, correo, rol FROM usuarios"
    ).fetchall()

    conexion.close()

    return jsonify([
        dict(usuario)
        for usuario in datos
    ])


@app.route("/usuarios/<int:id>")
def usuario(id):
    conexion = conectar_db()

    resultado = conexion.execute(
        """
        SELECT id, nombre, correo, rol
        FROM usuarios
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conexion.close()

    if resultado is None:
        return jsonify({
            "error": "Usuario no encontrado"
        }), 404

    return jsonify(dict(resultado))


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


if __name__ == "__main__":
    crear_tabla()

    app.run(
        debug=True,
        port=5002
    )