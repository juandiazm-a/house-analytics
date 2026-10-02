# House Analytics

House Analytics es un proyecto académico que desarrollamos para consultar y gestionar información sobre viviendas mediante una aplicación web.

Para realizar el proyecto utilizamos el dataset House Prices - Advanced Regression Techniques de Kaggle. De este dataset seleccionamos algunas variables que consideramos importantes para mostrar la información de las viviendas: precio, metros cuadrados, habitaciones y baños.

¿Qué hace el proyecto?

La aplicación permite consultar un catálogo de viviendas y utilizar filtros para encontrar registros según diferentes características.

También contamos con dos tipos de acceso:

- Usuario: puede iniciar sesión, consultar las viviendas y utilizar los filtros.
- Administrador: además de consultar las viviendas, puede agregar, editar y eliminar registros.

Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Git y GitHub
- Render

## Arquitectura

El proyecto está organizado utilizando un backend, un frontend y dos microservicios:

- Microservicio de viviendas
- Microservicio de usuarios

La comunicación entre las diferentes partes se realiza mediante APIs REST.

## Datos

Para la aplicación utilizamos una muestra de 30 viviendas del dataset original.

Las variables principales que utilizamos son:

| Dataset | Aplicación |
| SalePrice | Precio |
| GrLivArea | Metros cuadrados |
| BedroomAbvGr | Habitaciones |
| FullBath | Baños |

Los datos utilizados son históricos y se utilizan únicamente con fines académicos.

Funciones principales

La aplicación permite:

- Iniciar sesión como usuario.
- Consultar las viviendas.
- Filtrar las viviendas.
- Ver información de las propiedades.
- Iniciar sesión como administrador.
- Agregar viviendas.
- Editar viviendas.
- Eliminar viviendas.

## Estructura del proyecto

```text
house-analytics/
│
├── backend/
│
├── frontend/
│
└── services/
    ├── viviendas/
    └── usuarios/
