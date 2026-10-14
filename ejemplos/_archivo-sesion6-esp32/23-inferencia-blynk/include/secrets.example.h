// Plantilla de secrets.h — ESTE archivo sí se sube al repositorio.
//
// Cómo usarla:
//   1. Copia este archivo como include/secrets.h (mismo directorio).
//   2. En la consola de Blynk (https://blynk.cloud), en tu Template, crea dos
//      Datastreams de tipo Virtual Pin:
//        V2  «Gesto»      Integer, 0 a 2   (0 quieto, 1 giro, 2 vaiven)
//        V3  «Confianza»  Integer, 0 a 100 (unidad %)
//      Crea el dispositivo; en «Device Info» aparecen estas tres líneas.
//      Pégalas en secrets.h en lugar de los valores de ejemplo.
//
// secrets.h está en el .gitignore del proyecto: tu token nunca se sube.
// Quien tiene el token puede leer y mandar órdenes a TU dispositivo.
// Mientras no exista secrets.h, el proyecto compila con esta plantilla y el
// servidor de Blynk responde «Invalid auth token» (los LED funcionan igual).
#pragma once

#define BLYNK_TEMPLATE_ID "TMPLxxxxxxxx"
#define BLYNK_TEMPLATE_NAME "ESP32 PIT 2026"
#define BLYNK_AUTH_TOKEN "TU_TOKEN_AQUI"
