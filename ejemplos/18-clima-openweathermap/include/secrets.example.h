// Plantilla de secrets.h — ESTE archivo sí se sube al repositorio.
//
// Cómo usarla:
//   1. Copia este archivo como include/secrets.h (mismo directorio).
//   2. En secrets.h, reemplaza "TU_API_KEY_AQUI" por tu clave gratuita de
//      OpenWeatherMap (https://home.openweathermap.org/api_keys).
//
// secrets.h está en el .gitignore del proyecto: tu clave nunca se sube.
// Mientras no exista secrets.h, el proyecto compila con esta plantilla y la
// API responde 401 (clave inválida).
#pragma once

#define OWM_API_KEY "TU_API_KEY_AQUI"
