from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)

# Permitir conexiones desde el frontend
CORS(app)


# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "house_analytics.db"


# ==========================================
# CONEXIÓN CON LA BASE DE DATOS
# ==========================================

def conectar_db():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

    return jsonify({
        "mensaje": "API de House Analytics funcionando"
    })


# ==========================================
# LOGIN DE USUARIOS
# ==========================================

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


    # Usuarios de demostración
    usuarios = {

        "admin@houseanalytics.com": {
            "nombre": "Administrador",
            "rol": "administrador",
            "password": "admin123"
        },

        "usuario@houseanalytics.com": {
            "nombre": "Usuario Demo",
            "rol": "usuario",
            "password": "usuario123"
        }

    }


    usuario = usuarios.get(correo)


    if usuario is None or usuario["password"] != password:

        return jsonify({
            "error": "Correo o contraseña incorrectos"
        }), 401


    return jsonify({

        "mensaje": "Inicio de sesión correcto",

        "usuario": {

            "nombre": usuario["nombre"],

            "correo": correo,

            "rol": usuario["rol"]

        }

    })


# ==========================================
# OBTENER TODAS LAS VIVIENDAS
# ==========================================

@app.route("/api/viviendas")
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


# ==========================================
# OBTENER UNA VIVIENDA
# ==========================================

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


# ==========================================
# EDITAR UNA VIVIENDA
# ==========================================

@app.route(
    "/api/viviendas/<int:id>",
    methods=["PUT"]
)
def editar_vivienda(id):

    datos = request.get_json()

    if not datos:

        return jsonify({

            "error": "No se recibieron datos"

        }), 400


    precio = datos.get("Precio")

    area = datos.get("MetrosCuadrados")

    habitaciones = datos.get("Habitaciones")

    banos = datos.get("Banos")


    if (

        precio is None or

        area is None or

        habitaciones is None or

        banos is None

    ):

        return jsonify({

            "error": "Todos los campos son obligatorios"

        }), 400


    conexion = conectar_db()


    vivienda_existente = conexion.execute(

        "SELECT * FROM viviendas WHERE ID = ?",

        (id,)

    ).fetchone()


    if vivienda_existente is None:

        conexion.close()

        return jsonify({

            "error": "Vivienda no encontrada"

        }), 404


    conexion.execute(

        """

        UPDATE viviendas

        SET

            Precio = ?,

            MetrosCuadrados = ?,

            Habitaciones = ?,

            "Baños" = ?

        WHERE ID = ?

        """,

        (

            precio,

            area,

            habitaciones,

            banos,

            id

        )

    )


    conexion.commit()

    conexion.close()


    return jsonify({

        "mensaje": "Vivienda actualizada correctamente"

    })


# ==========================================
# AGREGAR UNA VIVIENDA
# ==========================================

@app.route(
    "/api/viviendas",
    methods=["POST"]
)
def agregar_vivienda():

    datos = request.get_json()

    if not datos:

        return jsonify({

            "error": "No se recibieron datos"

        }), 400


    precio = datos.get("Precio")

    area = datos.get("MetrosCuadrados")

    habitaciones = datos.get("Habitaciones")

    banos = datos.get("Banos")


    if (

        precio is None or

        area is None or

        habitaciones is None or

        banos is None

    ):

        return jsonify({

            "error": "Todos los campos son obligatorios"

        }), 400


    conexion = conectar_db()


    # Obtener el último ID

    resultado_id = conexion.execute(

        "SELECT MAX(ID) FROM viviendas"

    ).fetchone()


    ultimo_id = resultado_id[0]


    if ultimo_id is None:

        ultimo_id = 0


    nuevo_id = ultimo_id + 1


    # Insertar la nueva vivienda

    conexion.execute(

        """

        INSERT INTO viviendas

        (

            ID,

            Precio,

            MetrosCuadrados,

            Habitaciones,

            "Baños"

        )

        VALUES (?, ?, ?, ?, ?)

        """,

        (

            nuevo_id,

            precio,

            area,

            habitaciones,

            banos

        )

    )


    conexion.commit()

    conexion.close()


    return jsonify({

        "mensaje": "Vivienda agregada correctamente",

        "id": nuevo_id

    }), 201


# ==========================================
# ELIMINAR UNA VIVIENDA
# ==========================================

@app.route(
    "/api/viviendas/<int:id>",
    methods=["DELETE"]
)
def eliminar_vivienda(id):

    conexion = conectar_db()


    vivienda_existente = conexion.execute(

        "SELECT * FROM viviendas WHERE ID = ?",

        (id,)

    ).fetchone()


    if vivienda_existente is None:

        conexion.close()

        return jsonify({

            "error": "Vivienda no encontrada"

        }), 404


    conexion.execute(

        "DELETE FROM viviendas WHERE ID = ?",

        (id,)

    )


    conexion.commit()

    conexion.close()


    return jsonify({

        "mensaje": "Vivienda eliminada correctamente"

    })


# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":

    puerto = int(

        os.environ.get(

            "PORT",

            5000

        )

    )


    app.run(

        host="0.0.0.0",

        port=puerto,

        debug=False

    )