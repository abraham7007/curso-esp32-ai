#!/usr/bin/env python3
"""Tabla de terminología del curso: qué nombre lleva cada concepto.

EL CRITERIO, en una línea: **manda el término que usa el campo**, y en sistemas
embebidos ese término es muchas veces el inglés.

No se traduce por traducir. Un estudiante que sale de aquí va a leer la
documentación de Espressif, los mensajes del compilador y las preguntas de un
foro, y todo eso dice `timeout`, `polling` y `aliasing`. Traducirlos en clase lo
deja sin el vocabulario con el que se va a encontrar. Al revés también: hay
términos que en español están perfectamente asentados —pila, cola, trama,
condición de carrera— y ponerlos en inglés sería pedantería.

DÓNDE VA LA GLOSA EN ESPAÑOL. Solo donde el término inglés no se entiende por
sí solo: `aliasing (solapamiento espectral)`. Y solo en el CUERPO y en el
glosario —nunca en un título, que lleva el término a secas—. Glosar todo
sobrecarga la lámina y estorba justo a quien ya conoce el término.

Lo que NO entra en esta tabla: la sintaxis del lenguaje y los nombres de la
API. `millis()`, `pinMode()`, `#pragma once`, `NVS`, `LEDC` se escriben como los
imprime la herramienta, y eso nunca fue discutible.

Cada fila es (nombre_actual, nombre_nuevo, glosa). Glosa vacía = el término se
entiende sin ayuda y no lleva paréntesis.
"""

# Términos que pasan a su nombre original. Se listan por sesión para que la
# revisión pueda hacerse leyendo una sesión de golpe.
FLIPS = [
    # ── sesión 2 · C++ y organización
    ("Protección contra inclusión múltiple", "Include guard",
     "protección contra inclusión múltiple"),

    # ── sesión 3 · buses y formato de datos
    ("Velocidad en baudios", "Baud rate", "velocidad en baudios"),
    ("Dúplex completo", "Full duplex", ""),
    ("Resistencia de polarización", "Pull-up", "resistencia de polarización"),
    ("Línea de selección (CS)", "Chip select (CS)", "línea de selección"),
    ("Suma de comprobación", "Checksum", "suma de comprobación"),
    ("Orden de bytes", "Endianness", "orden de bytes"),
    ("Tiempo de espera", "Timeout", ""),

    # ── sesión 4 · adquisición y tratamiento
    ("Solapamiento espectral", "Aliasing", "solapamiento espectral"),
    ("Consulta periódica", "Polling", "consulta periódica"),
    ("Rutina de servicio de interrupción", "ISR",
     "rutina de servicio de interrupción"),
    ("Rebote de contacto", "Bouncing", "rebote de contacto"),
    ("Marca temporal", "Timestamp", ""),

    # ── sesión 5 · modelado del comportamiento
    ("Condición de guarda", "Guard", "condición de guarda"),
    ("Máquina jerárquica", "Statechart", "máquina de estados jerárquica"),

    # ── sesión 6 · concurrencia
    ("Interbloqueo", "Deadlock", "interbloqueo"),
    ("Afinidad de núcleo", "Core affinity", "afinidad de núcleo"),

    # ── sesión 8 · mensajería
    ("Calidad de servicio", "QoS", "calidad de servicio"),
    ("Mensaje retenido", "Retained message", "mensaje retenido"),
    ("Última voluntad", "Last Will", "mensaje de última voluntad"),
    ("Intervalo de mantenimiento", "Keepalive", "intervalo de mantenimiento"),

    # ── sesión 9 · servidor embebido
    ("Eventos enviados por el servidor", "Server-Sent Events (SSE)",
     "eventos enviados por el servidor"),
    ("Aprovisionamiento", "Provisioning", "aprovisionamiento"),
    ("Memoria no volátil", "NVS", "memoria no volátil"),
    ("Restablecimiento de fábrica", "Factory reset",
     "restablecimiento de fábrica"),

    # ── sesión 10 · robustez y mantenimiento
    ("Nivelado de desgaste", "Wear levelling", "nivelado de desgaste"),
    ("Causa del último reinicio", "Reset reason", "causa del último reinicio"),
    ("Sueño profundo", "Deep sleep", "sueño profundo"),
    ("Actualización remota", "OTA", "actualización remota"),
    ("Arranque seguro", "Secure boot", "arranque seguro"),

    # ── sesión 12 · aprendizaje automático embebido
    ("Poda", "Pruning", "poda"),
    ("Memoria de trabajo", "Tensor arena", "memoria de trabajo"),
    ("Deriva de la distribución", "Drift", "deriva de la distribución"),
]

# Verbos y sustantivos que NO son término técnico pero se eligieron mal en la
# primera redacción. No van en FLIPS porque no se traducen: se sustituyen por la
# palabra española que dice lo que pasa.
MAL_ELEGIDOS = {
    "gobernar / gobierno":
        "37 apariciones. «El ESP32 gobierna un LED», «gobierno de periféricos»: "
        "es un calco que en español no se usa para hardware. Se dice CONTROLAR "
        "y CONTROL. En los usos abstractos —«la distinción que gobierna el "
        "reintento», «el dispositivo no gobierna cuándo llegan las peticiones»— "
        "el verbo correcto es DECIDIR o DETERMINAR, no controlar: una "
        "sustitución uniforme habría empobrecido esas frases.",
}

# Términos que se QUEDAN en español, y por qué. Se escriben para que la próxima
# revisión no vuelva a plantearlos: están asentados en la literatura técnica en
# español y su forma inglesa no aporta nada.
SE_QUEDAN = {
    "Pila": "stack; «pila» es el término estándar en español",
    "Cola": "queue; igual de asentado",
    "Trama": "frame; estándar en telecomunicaciones",
    "Condición de carrera": "race condition; asentado",
    "Inversión de prioridad": "priority inversion; asentado",
    "Planificador expropiativo": "preemptive scheduler; asentado",
    "Compilación cruzada": "cross-compilation; asentado",
    "Encapsulamiento": "encapsulation; asentado",
    "Unidad de traducción": "translation unit; asentado",
    "Ciclo de trabajo": "duty cycle; asentado, y «duty» se usa de forma oral",
    "Entrada flotante": "floating input; transparente en español",
    "Portal cautivo": "captive portal; asentado",
    "Punto de acceso": "access point; asentado",
    "Matriz de confusión": "confusion matrix; asentado",
    "Cuantización": "quantization; asentado",
    "Superficie de ataque": "attack surface; asentado",
    "Media móvil": "moving average; asentado",
}
