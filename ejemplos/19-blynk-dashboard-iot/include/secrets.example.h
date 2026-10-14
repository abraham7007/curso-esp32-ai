// Plantilla de secrets.h — ESTE archivo sí se sube al repositorio.
//
// Cómo usarla:
//   1. Copia este archivo como include/secrets.h (mismo directorio).
//   2. En la consola de Blynk (https://blynk.cloud) crea tu Template y tu
//      dispositivo; en «Device Info» aparecen estas tres líneas. Pégalas en
//      secrets.h en lugar de los valores de ejemplo.
//
// secrets.h está en el .gitignore del proyecto: tu token nunca se sube.
// Quien tiene el token puede leer y mandar órdenes a TU dispositivo.
// Mientras no exista secrets.h, el proyecto compila con esta plantilla y el
// servidor de Blynk responde «Invalid auth token».
#pragma once

#define BLYNK_TEMPLATE_ID "TMPLxxxxxxxx"
#define BLYNK_TEMPLATE_NAME "ESP32 PIT 2026"
#define BLYNK_AUTH_TOKEN "TU_TOKEN_AQUI"
