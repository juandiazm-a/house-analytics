import sqlite3
import pandas as pd

# Cargar el catálogo
df = pd.read_csv("catalogo_viviendas.csv")

# Conectar con SQLite
conexion = sqlite3.connect("house_analytics.db")

# Guardar las viviendas en la base de datos
df.to_sql(
    "viviendas",
    conexion,
    if_exists="replace",
    index=False
)

conexion.close()

print("Base de datos creada correctamente.")
print("Tabla 'viviendas' creada con", len(df), "registros.")