# ==================================
# PROYECTO BIENES RAÍCES
# ==================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv("Proyecto 3/train.csv")

# EXPLORACIÓN INICIAL

print(df.head())

print("\nDimensiones:")
print(df.shape)

print("\nInformación:")
print(df.info())

print("\nValores nulos:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

# LIMPIEZA BÁSICA

df = df.drop_duplicates()

# VARIABLES IMPORTANTES

variables = [
    'SalePrice',
    'GrLivArea',
    'BedroomAbvGr',
    'FullBath',
    'YearBuilt',
    'LotArea',
    'GarageCars'
]

# CORRELACIONES

corr = df[variables].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr,
            annot=True,
            cmap='coolwarm')

plt.title("Correlación entre variables")
plt.show()

# TAMAÑO VS PRECIO

plt.figure(figsize=(8,5))
sns.scatterplot(
    x='GrLivArea',
    y='SalePrice',
    data=df
)

plt.title("Área habitable vs Precio")
plt.show()

# HABITACIONES VS PRECIO

plt.figure(figsize=(8,5))
sns.boxplot(
    x='BedroomAbvGr',
    y='SalePrice',
    data=df
)

plt.title("Habitaciones vs Precio")
plt.show()


# BAÑOS VS PRECIO

plt.figure(figsize=(8,5))
sns.boxplot(
    x='FullBath',
    y='SalePrice',
    data=df
)

plt.title("Baños vs Precio")
plt.show()

# TERRENO VS PRECIO

plt.figure(figsize=(8,5))
sns.scatterplot(
    x='LotArea',
    y='SalePrice',
    data=df
)

plt.title("Área del terreno vs Precio")
plt.show()


# GARAJE VS PRECIO

plt.figure(figsize=(8,5))
sns.boxplot(
    x='GarageCars',
    y='SalePrice',
    data=df
)

plt.title("Capacidad del garaje vs Precio")
plt.show()

# VECINDARIOS MÁS CAROS

vecindarios = (
    df.groupby('Neighborhood')['SalePrice']
    .mean()
    .sort_values(ascending=False)
)

print("\nVecindarios más caros:")
print(vecindarios.head(10))

plt.figure(figsize=(12,6))
vecindarios.head(10).plot(kind='bar')
plt.title("Top 10 vecindarios con mayor precio promedio")
plt.ylabel("Precio promedio")
plt.show()

# ----------------------------------
# VARIABLES MÁS RELACIONADAS
# ----------------------------------

correlacion_precio = corr['SalePrice'].sort_values(ascending=False)

print("\nCorrelación con el precio:")
print(correlacion_precio)