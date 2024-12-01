# CEDICA - Administración

## Introducción
Bienvenido al proyecto "CEDICA - Administración". Este documento proporciona los pasos necesarios para montar la base de datos en producción y levantar la aplicación.

## Montar la Base de Datos

### Creación de tablas e inserción de datos de prueba
1. Usa los scripts de DB_setup para crear y cargar las siguientes tablas en este orden:
    1. `permissions`
    2. `roles`
    3. `role_permissions`
    4. `user`
2. Inicia sesión en la aplicación con las siguientes credenciales:
    - **Usuario**: `admin@admin.com`
    - **Contraseña**: `admin`
3. Escribe el dominio del sitio seguido de el path /resources/seeds.
4. Espera a que se complete el script.
5. Opcionalmente puedes truncar las tablas `provinces` y `localities` y cargar las que se encuentran en DB_setup, que contienen más ciudades.

## Pasos para Levantar la Aplicación

### En Producción
1. Configura las variables de entorno necesarias en Vault (para la BD, MinIO y Google).
2. Ejecuta el pipeline `deploy-backend` en la rama `main`.
3. Crea las tablas como se ha visto en la sección anterior.

### En Desarrollo
1. Configura las variables de entorno para la base de datos PostgreSQL y MinIO en el archivo `.env`. Ambas están definidas en `src/core/config.py`.
2. Ejecuta el comando:
    ```bash
    poetry install --with=dev
    ```
3. Inicia una shell de Poetry:
    ```bash
    poetry shell
    ```
4. Resetea la base de datos y siembra los datos:
    ```bash
    flask reset-db && flask seeds-db
    ```
    o simplemente ejecuta el script como en producción

5. Levanta la aplicación:
    ```bash
    flask run
    ```
    o

    ```bash
    flask run --debug
    ```

    La aplicación estará disponible en `http://localhost:5000`

## Credenciales importantes
1. **Administrador**:
    - **Roles**: `SystemAdmin`
    - **Email**: `admin@admin.com`
    - **Contraseña**: `admin`

2. **Giu**:
    - **Roles**: `Administracion`
    - **Email**: `giuliana@gmail.com`
    - **Contraseña**: `123`

3. **Eze (Todos los permisos)**:
    - **Roles**: `Tecnica` `Ecuestre` `Voluntariado` `Administracion` `SystemAdmin`
    - **Email**: `eze@gmail.com`
    - **Contraseña**: `123`

¡Gracias por utilizar el proyecto CEDICA - Administración!