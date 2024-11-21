# CEDICA - Portal Público

## Introducción

Bienvenido al proyecto **CEDICA - Portal Público**. Este portal tiene como objetivo principal mostrar información al público general, como noticias, actividades y eventos, y también enviar mensajes con dudas o sugerencias al staff. La aplicación consume una API gestionada por **CEDICA - Administración**.

Este documento describe cómo instalar las dependencias, iniciar la aplicación y detalla algunos requisitos esenciales.

## Requisitos Previos

1. **Node** (versión 22.7.0).
2. **NPM** o **Yarn** como gestor de paquetes.
3. API de **CEDICA - Administración** en funcionamiento.

## Configuración del Proyecto

### Instalación de Dependencias
Instala las dependencias necesarias con:
```bash
npm install
```

## Pasos para Iniciar la Aplicación

### En Producción
Ejecuta el pipeline `deploy-frontend` en la rama `main`.

### En Desarrollo

Ejecuta el siguiente comando para iniciar el servidor en modo desarrollo con hot-reload:
```bash
npm run dev
```

El portal estará disponible en `http://localhost:5173`.

## Consideraciones Importantes

**Dependencia de la API**: Este portal requiere que la API de administración esté funcionando y tenga datos cargados en la tabla `articles`. De lo contrario, el portal no mostrará noticias ni actividades.

¡Gracias por utilizar el proyecto **CEDICA - Portal Público**!
