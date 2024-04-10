# YouLikeHitsBot

## Descripción

`YouLikeHitsBot` es un bot automatizado diseñado para interactuar con videos de YouTube a través de la plataforma YouLikeHits. Su objetivo principal es **automatizar el proceso de hacer clic en videos para acumular puntos** en la página. Cada instancia del bot opera de forma independiente, permitiendo a los usuarios escalar el número de puntos generados simultáneamente.

## Configuración

Antes de iniciar el bot, **es necesario configurar tus credenciales de YouLikeHits**. Esto se hace proporcionando tu nombre de usuario y contraseña en un archivo `.env` en el directorio raíz del proyecto. Sigue estos pasos:

1. Crea un archivo `.env` en el directorio raíz del proyecto, si aún no existe.
2. Añade las siguientes líneas al archivo `.env`, reemplazando `your_username_here` y `your_password_here` con tu nombre de usuario y contraseña de YouLikeHits, respectivamente:

    ```
    YOULIKEHITS_USERNAME=your_username_here
    YOULIKEHITS_PASSWORD=your_password_here
    ```

## Ejecución

Para **iniciar el programa con 3 bots independientes**, cada uno destinado a generar puntos, usa el siguiente comando en la terminal:

```bash
docker-compose up --build --scale app_instance=3 -d
```

Este comando construirá las imágenes necesarias (si es la primera vez o si se han hecho cambios en el código o dependencias) y luego iniciará tres instancias del bot en modo "detached", permitiéndote continuar usando la terminal mientras los bots están en ejecución.

## Nota

Este bot está diseñado para fines educativos y de demostración. **Asegúrate de usarlo de manera responsable** y conforme a las políticas y términos de servicio de YouLikeHits y YouTube.