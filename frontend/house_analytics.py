# ==================================
# HOUSE ANALYTICS
# ==================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv("train.csv")

# EXPLORACIÓN INICIAL

print("Primeras filas:")
print(df.head())

print("\nDimensiones:")
print(df.shape)

print("\nInformación:")
print(df.info())

print("\nValores nulos:")
print(df[['SalePrice', 'GrLivArea', 'BedroomAbvGr', 'FullBath']].isnull().sum())

# LIMPIEZA

df = df.drop_duplicates()

# VARIABLES DEL PROYECTO

variables = [
    'SalePrice',
    'GrLivArea',
    'BedroomAbvGr',
    'FullBath'
]

# Crear nuevo DataFrame solamente con las variables que necesitamos

viviendas = df[variables].copy()

print("\nDatos utilizados en House Analytics:")
print(viviendas.head())

# CORRELACIÓN

corr = viviendas.corr()

plt.figure(figsize=(8, 6))

sns.heatmap(
    corr,
    annot=True,
    cmap='coolwarm'
)

plt.title("Relación entre las características de las viviendas")
plt.show()

# METROS CUADRADOS VS PRECIO

plt.figure(figsize=(8, 5))

sns.scatterplot(
    x='GrLivArea',
    y='SalePrice',
    data=viviendas
)

plt.title("Metros cuadrados vs Precio")
plt.xlabel("Metros cuadrados")
plt.ylabel("Precio")
plt.show()

# HABITACIONES VS PRECIO

plt.figure(figsize=(8, 5))

sns.boxplot(
    x='BedroomAbvGr',
    y='SalePrice',
    data=viviendas
)

plt.title("Habitaciones vs Precio")
plt.xlabel("Habitaciones")
plt.ylabel("Precio")
plt.show()

# BAÑOS VS PRECIO

plt.figure(figsize=(8, 5))

sns.boxplot(
    x='FullBath',
    y='SalePrice',
    data=viviendas
)

plt.title("Baños vs Precio")
plt.xlabel("Baños")
plt.ylabel("Precio")
plt.show()

# INFORMACIÓN GENERAL

print("\nPrecio promedio:")
print(viviendas['SalePrice'].mean())

print("\nMetros cuadrados promedio:")
print(viviendas['GrLivArea'].mean())

print("\nHabitaciones promedio:")
print(viviendas['BedroomAbvGr'].mean())

print("\nBaños promedio:")
print(viviendas['FullBath'].mean())

# ELIMINAR DATOS VACÍOS
viviendas = viviendas.dropna()

# SELECCIONAR 30 VIVIENDAS
catalogo = viviendas.sample(
    n=30,
    random_state=42
).reset_index(drop=True)

# CAMBIAR NOMBRES DE LAS COLUMNAS
catalogo = catalogo.rename(columns={
    'SalePrice': 'Precio',
    'GrLivArea': 'MetrosCuadrados',
    'BedroomAbvGr': 'Habitaciones',
    'FullBath': 'Baños'
})

# CREAR ID PARA CADA VIVIENDA
catalogo.insert(0, 'ID', range(1, 31))

print("\nCATÁLOGO DE 30 VIVIENDAS")
print(catalogo)

# GUARDAR CATÁLOGO
catalogo.to_csv("catalogo_viviendas.csv", index=False)

print("\nCatálogo guardado correctamente.")