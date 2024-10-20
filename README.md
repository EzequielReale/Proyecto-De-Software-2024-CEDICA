# CEDICA - Administración

## Introducción
Bienvenido al proyecto "CEDICA - Administración". Este documento proporciona los pasos necesarios para montar la base de datos en producción, levantar la aplicación y detalla algunos problemas conocidos.

## Orden para montar la Base de Datos en producción

### Creación de Tablas
1. **Tablas Auxiliares**:
    - `provinces`
    - `activities`
    - `localities` (después de `provinces`)
    - `disability_types`
    - `disability_diagnoses` (después de `disability_types`)
    - etc.

2. **Tablas Complementarias**:
    - `persons`
    - `permissions`
    - `roles`
    - `tutors`
    - etc.

3. **Tablas Relevantes**:
    - `members`
    - `riders`
    - `horses`
    - `person_documents`
    - `horse_documents`
    - etc.

4. **Tablas de Relaciones**:
    - `rider_member`
    - `role_permissions`
    - `user_roles`
    - etc.

### Inserción de Datos
Una vez creadas las tablas, ejecuta los `INSERT INTO` correspondientes en el mismo orden:

1. Tablas Auxiliares
2. Tablas Complementarias
3. Tablas Relevantes
4. Tablas de Relaciones

## Pasos para Levantar la Aplicación

### En Producción
1. Configura la Base de Datos como se te ha enseñado.
2. Ejecuta el pipeline en la rama `main`.

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
5. Levanta la aplicación:
    ```bash
    flask run
    ```
    o

    ```bash
    flask run --debug
    ```

## Known issues
- **Frontend**: Al ser Nicolás nuestro único desarrollador frontend, es posible que algunas partes de este, no hechas por él, puedan estar mejor diseñadas o mantener mejor el estado. Hemos intentado hacer lo mejor posible con los conocimientos que tenemos.
- **Integraciones Pendientes**: Algunas integraciones se harán después de la entrega para evitar errores inesperados en producción. Por ejemplo:
    - Integrar el campo `institutional_work_proposal` (que actualmente es un enum) como una referencia a `activities`.
    - Consolidar los documentos de la persona y del caballo en un solo modelo `documents`.
    - A mitad del desarrollo, se agregó un módulo de funciones genéricas para la base de datos, pero probablemente no hayamos llegado a refactorizar todo el código como nos hubiera gustado.
- **Patrones de Diseño**: Para el filtrado, podrían haberse usado patrones de diseño que simplifiquen el código. Sin embargo, decidimos dejarlo como está ya que el código actual funciona, es relativamente eficiente y está comentado, aunque sea largo.

¡Gracias por utilizar el proyecto CEDICA - Administración!