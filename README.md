# CEDICA

Bienvenido al repositorio del proyecto para **CEDICA**. Este repositorio alberga dos proyectos principales:

1. **CEDICA - Administración**: Una aplicación backend diseñada para gestionar el contenido y las operaciones internas de la organización.
2. **CEDICA - Portal Público**: Una aplicación frontend que muestra noticias, actividades y eventos al público general, y permite enviar mensajes al staff.

## Requisitos Generales

1. **Git** para clonar y gestionar el repositorio.
2. **Node.js** (versión 22.7.0) para ejecutar el frontend.
3. **Python** (versión 3.12) para ejecutar el backend.

---

## Pasos para Clonar y Configurar el Repositorio

1. Clona el repositorio:
    ```bash
    git clone https://gitlab.catedras.linti.unlp.edu.ar/proyecto2024/proyectos/grupo04/code.git
    cd CODE
    ```

2. Sigue las instrucciones específicas para cada proyecto en sus respectivos directorios:
   - **Administración**: [Instrucciones detalladas](./admin/README.md)
   - **Portal Público**: [Instrucciones detalladas](./portal/README.md)

---

## Despliegue

### En Producción

Ambos proyectos cuentan con pipelines automatizados para despliegue en producción:

1. **Backend**: Ejecuta el pipeline `deploy-backend` en la rama `main` para desplegar la API de administración.
2. **Frontend**: Ejecuta el pipeline `deploy-frontend` en la rama `main` para desplegar el portal público.

### En Desarrollo

Levanta cada proyecto de manera local siguiendo las instrucciones individuales.

---

## Dependencias entre Proyectos

- **CEDICA - Portal Público** depende de la API de administración para mostrar datos como noticias y actividades, o enviar mensajes.
- Antes de iniciar el portal público, asegúrate de que el backend esté operativo y, preferentemente, con datos cargados.

---

## Advertencias

Asegúrate de que las tablas necesarias estén llenas antes de probar funcionalidades dependientes de datos (como `estadísticas` o `noticias y actividades`).

---

¡Gracias por colaborar con **CEDICA**!