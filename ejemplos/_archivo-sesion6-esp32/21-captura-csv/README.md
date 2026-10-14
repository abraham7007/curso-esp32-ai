# Ejemplo 21 · Captura CSV etiquetada

El ESP32 imprime una línea CSV por ventana (cada 0,5 s):

```
sesion,ventana,etiqueta,media,desv,rango,cruces
9f3a01c2,1,quieto,2047.3,3.21,12,0
```

- **sesion**: número hexadecimal aleatorio, distinto en cada arranque. Permite separar entrenamiento y prueba por sesión.
- **etiqueta**: el gesto que elegiste con el pulsador del GPIO 4 (quieto → giro → vaiven → quieto…). Al pulsar, la ventana se vacía y el primer dato del gesto nuevo llega 1 s después.
- Las líneas que empiezan por `#` no son datos: cambios de etiqueta (`#ETIQUETA giro`) y el balance cada 20 ventanas (`#BALANCE quieto=12 giro=5 vaiven=3 razon=4.0:1 AVISO…`).

## Cómo guardarlo en un archivo

**Placa real (PlatformIO):**

```
pio device monitor -b 115200 -f log2file
```

Todo lo que llega se guarda también en un archivo `platformio-device-monitor-<fecha>.log` en la carpeta del proyecto. Haz los gestos, cambia de etiqueta con el pulsador y cierra el monitor con `Ctrl+C`.

**Wokwi (wokwi.com):** selecciona el texto del monitor serie, cópialo y pégalo en un archivo de texto.

## Antes de entrenar

1. Graba **varias sesiones** (reinicia la placa entre una y otra: cada arranque es una sesión nueva). Mejor si son días o personas distintas.
2. Vigila `#BALANCE`: si una clase tiene más de 3 veces las ventanas de otra, captura más de la que falta.
3. Junta todos los registros en un solo archivo, llámalo `gestos.csv` y cópialo en `ejemplos/22-entrenar-exportar/entrenamiento/`, en lugar del `gestos.csv` sintético que trae. No hace falta limpiarlo: `entrenar.py` ignora las líneas `#`, las cabeceras repetidas (una por arranque) y el texto de arranque del ESP32, y avisa de cuántas líneas descartó.
