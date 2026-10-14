# Archivo · ejemplos ESP32 de la sesión 6 anterior

Estos cuatro proyectos eran los ejemplos de la sesión 6 (TinyML) cuando la sesión se daba con el ESP32 y un potenciómetro:

| Proyecto | Qué hacía |
|---|---|
| `20-umbral-ventana` | Ventana deslizante sobre el potenciómetro y una regla de umbral fijo. |
| `21-captura-csv` | Captura de características etiquetadas por el puerto serie. |
| `22-entrenar-exportar` | Árbol y bosque con scikit-learn, exportados a C con emlearn. |
| `23-inferencia-blynk` | Inferencia en vivo en el ESP32 y publicación en Blynk. |

**Se reemplazaron** (14-oct-2026) por los ejemplos de la **Arduino Nano 33 BLE Sense Rev2** con TensorFlow Lite Micro:

- `ejemplos/20-gestos-imu-nano33` (gestos con el IMU, modelo float).
- `ejemplos/21-colores-apds9960-nano33` (colores con el APDS9960, modelo cuantizado int8).

Se guardan aquí como referencia y ya no están registrados en `esp32.code-workspace`. Siguen compilando por separado (`pio run -d <carpeta>`), pero el material del estudiante no los cita.
