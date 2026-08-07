# Artículos de referencia del curso

Todos son de acceso abierto y se descargaron con `tools/get-paper.py`, que
resuelve el DOI contra Unpaywall y Europe PMC y verifica que lo recibido sea
realmente un PDF.

Antes de usar uno en una lámina: **leerlo completo**. El resumen no basta para
enunciar un procedimiento experimental ni una conclusión. Las reglas de la
lámina de artículo están en `.claude/skills/presentation-design/SKILL.md`.

---

## Clase 1 — Fundamentos del ESP32 · **integrados en las láminas**

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `caracterizacion-esp32-sensores.pdf` | Espinosa-Gavira et al. (2024). Characterization and Performance Evaluation of ESP32 for Real-time Synchronized Sensor Networks. *Procedia Comput. Sci.* 237, 261-268. `10.1016/j.procs.2024.05.104` | CC BY-NC-ND | Conversión ADC · Ejemplo 03 |
| `emulacion-qemu-esp32.pdf` | Howard & Irvin (2023). ESP32: QEMU Emulation within a Docker Container. `arXiv:2303.10204` | CC BY | Cadena de construcción · Flasheo |
| `llm-programacion-microcontroladores.pdf` | Babiuch & Smutný (2026). Benchmarking LLMs for Embedded Systems Programming. *Future Internet* 18(2), 94. `10.3390/fi18020094` | CC BY | La hora del código · Diagnóstico |
| `embedagent-llm-embebidos.pdf` | Xu et al. (2026). EmbedAgent. *ICSE '26*. `arXiv:2506.11003` | CC BY | La hora del código · Wokwi |

---

## Clase 2 — Arquitectura de firmware y programación

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `arquitectura-firmware-independiente.pdf` | Farina et al. (2024). Hardware-Independent Embedded Firmware Architecture Framework. *J. Internet Serv. Appl.* 15(1). `10.5753/jisa.2024.3634` | CC BY | Modelo de tres capas · lib frente a src · Estructura del proyecto |
| `rust-vs-c-firmware.pdf` | Thapa et al. (2026). Embedded Rust or C Firmware? Lessons from an Industrial Microcontroller Use Case. `arXiv:2604.25679` | CC BY | Tipos explícitos · Punteros y referencias · Tipos de error |
| `defectos-software-embebido-codeql.pdf` | Yuan & Davis et al. (2023). Finding 709 Defects in 258 Projects. `arXiv:2310.00205` | CC BY | Tipos de error · Problemas frecuentes |
| `pruebas-hardware-in-the-loop.pdf` | Kaspar et al. (2021). PHiLIP on the HiL. `arXiv:2107.07255` | CC BY | Encapsulamiento · Interfaz común · Por qué se separa en capas |
| `calidad-proyectos-arduino.pdf` | Corno & Mannella (2023). Security Evaluation of Arduino Projects Developed by Hobbyist IoT Programmers. *Sensors* 23(5), 2740. `10.3390/s23052740` | CC BY | Control de versiones · Constantes con nombre · Problemas frecuentes |
| `lenguajes-esp32-rendimiento.pdf` | Plauska, Liutkevičius & Janavičiūtė (2023). Performance Evaluation of C/C++, MicroPython, Rust and TinyGo Programming Languages on ESP32 Microcontroller. *Electronics* 12(1), 143. `10.3390/electronics12010143` | CC BY | Elección del lenguaje · Coste de la abstracción · **medido sobre ESP32** |

---

## Clase 3 — Comunicación serie y buses

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `controlador-i2c-bajo-consumo.pdf` | (2026). Low-power design and implementation of an enhanced I2C bus controller using OpenLane. *Scientific Reports*. `10.1038/s41598-026-53211-1` | CC BY | Bus I²C · Criterios de selección |
| `vulnerabilidades-bus-i2c.pdf` | (2017). Plataforma experimental para el estudio de vulnerabilidades hardware en robots móviles: bus I²C. *Rev. Iberoam. Autom. Inform. Ind.* `10.1016/j.riai.2017.02.002` | CC BY-NC-ND | Bus I²C · Masa común · Niveles lógicos — **en español** |
| `controlador-spi-flash.pdf` | Li et al. (2024). A Lightweight SPI-Flash Controller Based on AMBA AHB-Lite Bus. *Micromachines* 15(10), 1246. `10.3390/mi15101246` | CC BY | Bus SPI · Comparador I²C/SPI |
| `fiabilidad-uart-usb.pdf` | (2022). The reliability of serial data communication using UART-USB converter. *Zbornik Radova*. `10.5937/zeint32-41677` | CC BY | Trama UART · Desajuste de baudios · Tiempos de espera |
| `crc-deteccion-errores-tramas.pdf` | (2020). Implementing Cyclic Redundancy Check as Error Correction Technique in HDLC. *Ann. Comput. Sci. Inf. Syst.* `10.15439/2020KM13` | CC BY | Trama propia · Constructor de tramas · Verificación |
| `pson-serializacion-sensores.pdf` | Luis et al. (2021). PSON: A Serialization Format for IoT Sensor Networks. *Sensors* 21(13), 4559. `10.3390/s21134559` | CC BY | JSON · Orden de bytes · Ejemplo 14 |

---

## Clase 4 — Sensores, adquisición e interrupciones

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `calibracion-sensor-co2-campo.pdf` | Brown et al. (2020). Low cost CO₂ sensing: a simple microcontroller approach with calibration and field use. *HardwareX* 8, e00136. `10.1016/j.ohx.2020.e00136` | CC BY | Calibración · Validación del dato · Cadena de tratamiento |
| `adquisicion-multicanal-esp32.pdf` | Zobel, Maierhofer & Rixen (2026). OASIS-ERIS: Open Acquisition System for IEPE Sensors. `arXiv:2607.22061` | CC BY | Cadena de tratamiento · Muestreo · Temporizadores · **ESP32-S3 + ADC externo de 18 bits a 100 kHz** |
| `arquitectura-daq-esp32.pdf` | (2026). A Systems-Engineered ESP32 DAQ Architecture and FAIR Data Workflow. `arXiv:2601.03867` | CC BY | Interfaz común de driver · Marca temporal · Ejemplo 19 |
| `interrupciones-tareas-tiempo-real.pdf` | (2021). Interrupting Real-Time IoT Tasks: How Bad Can It Be to Connect Your Critical Embedded System to the Internet? `arXiv:2102.05559` | CC BY | Consulta frente a interrupción · Requisitos de la ISR · Presupuesto del bucle |
| `sincronizacion-tiempo-esp32.pdf` | Gundall et al. (2025). Benchmarking OpenWiFiSync on ESP32. `arXiv:2511.14457` | CC BY | Marca temporal · Sincronización entre nodos |

---

## Clase 5 — Máquinas de estados finitos

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `fsm-equipo-medico.pdf` | Baroudi et al. (2025). State machine design for an automated peritoneal dialysis machine. *Front. Med. Technol.* 7. `10.3389/fmedt.2025.1630829` | CC BY | Modelado del comportamiento · Estados y transiciones · **Caso donde un estado mal cerrado tiene consecuencia clínica** |
| `petri-net-arduino.pdf` | Kučera et al. (2019). PN2ARDUINO: A New Petri Net Software Tool for Control of Discrete-Event and Hybrid Systems. *Ann. Comput. Sci. Inf. Syst.* 18, 915-919. `10.15439/2019F20` | CC BY-NC-ND | Del diagrama al código · Herramientas de modelado |
| `composicion-statecharts.pdf` | Graics et al. (2020). Mixed-semantics composition of statecharts for the component-based design of reactive systems. *Softw. Syst. Model.* 19(6), 1483-1517. `10.1007/s10270-020-00806-5` | CC BY | Composición de máquinas · Sistemas reactivos |
| `statecharts-uml-jerarquicos.pdf` | Carnevali et al. (2022). Compositional Analysis of Hierarchical UML Statecharts. *IEEE Trans. Softw. Eng.* 48(12). `10.1109/TSE.2021.3125720` | CC BY | Estados jerárquicos · Verificación del modelo |
| `fsm-ortesis-wifi.pdf` | Kotsiubailo & Lysenko (2026). WiFi-Based Control System for Active Lower Limb Orthosis. *Microsyst. Electron. Acoust.* 31(1). `10.20535/2523-4455.mea.355559` | CC BY | Aplicación · Puente con la sesión 7 |

---

## Clase 6 — FreeRTOS y ejecución concurrente

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `freertos-esp32-multinucleo.pdf` | Arm, Baštán, Mihálik & Bradáč (2022). Measuring the Performance of FreeRTOS on ESP32 Multi-Core. *IFAC-PapersOnLine* 55(4), 292-297. `10.1016/j.ifacol.2022.06.048` | CC BY-NC-ND | **El artículo de referencia de la sesión** · Cambio de contexto y jitter medidos sobre ESP32-WROOM-32 · Coste de replanificar al otro núcleo · Los dos núcleos |
| `sobrecarga-freertos-tareas.pdf` | Miranda et al. (2021). Analysis of FreeRTOS Overheads on Periodic Tasks. *Anais do XX WPerformance*, 119-130. `10.5753/wperformance.2021.15728` | CC BY | **Coste real del planificador** · Tareas periódicas · Por qué una tarea no es gratis |
| `iotst-trazas-planificador.pdf` | Salles & Farias (2023). TLS Protocol Analysis Using IoTST: An IoT Benchmark Based on Scheduler Traces. *Sensors* 23(5), 2538. `10.3390/s23052538` | CC BY | Trazas del planificador · Medición del tiempo de tarea |
| `sincronizacion-no-bloqueante.pdf` | Ruiz et al. (2020). Non-Blocking Synchronization Between Real-Time and Non-Real-Time Applications. *IEEE Access* 8, 147618-147634. `10.1109/ACCESS.2020.3015385` | CC BY | Comunicación entre tareas · Colas · Por qué no basta una variable compartida |
| `freertos-modos-bajo-consumo.pdf` | Liubimov & Turkin (2024). Estudio experimental de la reactividad de FreeRTOS en modos de ahorro de energía. *Aerosp. Tech. Technol.* (4), 71-86. `10.32620/aktt.2024.4.09` | CC BY | Latencia de respuesta · Consumo · (texto en ucraniano; figuras y tablas legibles) |
| `freertos-domotica-comparativa.pdf` | Gao (2025). A Comparative Study of an STM32F103C8T6-Based FreeRTOS Smart Home System. *Informatica* 49(24), 401-416. `10.31449/inf.v49i24.11427` | CC BY | Aplicación completa con tareas · Reparto de responsabilidades |

---

## Clase 7 — Redes TCP/IP y HTTP

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `protocolos-mensajeria-iot.pdf` | Naik (2017). Choice of effective messaging protocols for IoT systems: MQTT, CoAP, AMQP and HTTP. *IEEE ISSE 2017*, 1-7. `10.1109/SysEng.2017.8088251` | Copia de repositorio | **Criterio para elegir protocolo** · Comparación de los cuatro · Puente con la sesión 8 |
| `mqtt-vs-http-esp32.pdf` | Adriansyah et al. (2026). Performance Analysis of MQTT and HTTP Protocols on Low-Power ESP32 Devices. *CoreID J.* 4(1), 38-45. `10.60005/coreid.v4i1.160` | CC BY | **Medido sobre ESP32** · Latencia y consumo de HTTP frente a MQTT |
| `dispositivos-iot-esp32.pdf` | Hercog et al. (2023). Design and Implementation of ESP32-Based IoT Devices. *Sensors* 23(15), 6739. `10.3390/s23156739` | CC BY | ESP32 como cliente · Arquitectura del dispositivo |
| `cifrado-rsa-ecc-iot.pdf` | Suárez-Albela et al. (2018). A Practical Evaluation on RSA and ECC-Based Cipher Suites for IoT. *Sensors* 18(11), 3868. `10.3390/s18113868` | CC BY | HTTPS y TLS · Coste del cifrado en un microcontrolador |
| `antena-adaptativa-esp32-web.pdf` | Kodera (2018). Adaptive antenna system by ESP32-PICO-D4 and its application to web radio system. *HardwareX* 3, 91-99. `10.1016/j.ohx.2018.03.001` | CC BY | Servidor web en el ESP32 · Aplicación |

---

## Clase 8 — MQTT y plataformas de IoT

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `mqtt-m2m-revision.pdf` | Mishra & Kertesz (2020). The Use of MQTT in M2M and IoT Systems: A Survey. *IEEE Access* 8, 201071-201086. `10.1109/ACCESS.2020.3035849` | Dominio público | **Panorámica del protocolo** · Publicación-suscripción · Niveles de QoS |
| `plataformas-nube-iot-comparativa.pdf` | Pierleoni et al. (2020). Amazon, Google and Microsoft Solutions for IoT: Architectures and a Performance Comparison. *IEEE Access* 8, 5455-5470. `10.1109/ACCESS.2019.2961511` | CC BY | **Elección de plataforma** · Arquitectura de sistema · Comparación medida |
| `mqtt-latencia-borde-nube.pdf` | Tseng et al. (2025). Cloud-edge MQTT messaging for latency mitigation and broker memory footprint reduction. *PeerJ Comput. Sci.* 11, e2741. `10.7717/peerj-cs.2741` | CC BY | Dónde colocar el broker · Latencia · Memoria |
| `brokers-mqtt-distribuidos.pdf` | Kosaka et al. (2023). Implementation and Evaluation of the Control Mechanism Among Distributed MQTT Brokers. *IEEE Access* 11, 134211-134216. `10.1109/ACCESS.2023.3335273` | CC BY | Escala del sistema · Varios brokers |
| `estres-servidor-mqtt.pdf` | Hijazi et al. (2021). Stress Testing MQTT Server for Private IoT Networks. *Int. J. Electron. Telecommun.* 67(2), 229-234. `10.24425/ijet.2021.135969` | CC BY | Límites del broker · Cuántos dispositivos aguanta |

---

## Clase 9 — Servidor web embebido, aprovisionamiento e integración en un producto

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `nist-incorporacion-dispositivos.pdf` | Symington et al. (2020). Trusted IoT Device Network-Layer Onboarding and Lifecycle Management. *NIST Cybersecurity White Paper* (borrador). `10.6028/NIST.CSWP.09082020-draft` | Dominio público | **Marco de referencia del aprovisionamiento** · Ciclo de vida del dispositivo · Restablecimiento de fábrica |
| `aprovisionamiento-seguro-iot.pdf` | Kanciak et al. (2022). Secure Onboarding and Key Management in Federated IoT Environments. *Ann. Comput. Sci. Inf. Syst.* 30, 627-634. `10.15439/2022F173` | CC BY | Entrega de credenciales · Por qué no se incrustan en el binario |
| `aprovisionamiento-autenticacion-fiware.pdf` | Sousa et al. (2021). Provisioning, Authentication and Secure Communications for IoT Devices on FIWARE. *Sensors* 21(17), 5898. `10.3390/s21175898` | CC BY | Identidad del dispositivo · Autenticación · Puente con la sesión 8 |
| `etiquetado-seguridad-producto.pdf` | Johnson et al. (2020). The impact of IoT security labelling on consumer product choice and willingness to pay. *PLOS ONE* 15(1), e0227800. `10.1371/journal.pone.0227800` | CC BY | **Contenido de la etiqueta** · Requisitos de un producto comercializable · Estudio con consumidores reales |
| `sistema-esp32-invernadero.pdf` | Correa-Quiroz et al. (2025). IoT System with ESP32 for Smart Drip Irrigation and Climate Monitoring in Greenhouses. *Emerg. Sci. J.* 9(3), 1133-1157. `10.28991/esj-2025-09-03-01` | CC BY | Sistema ESP32 completo en operación · Caso de integración |

También aplicables, ya descargados en otra clase: `dispositivos-iot-esp32.pdf`
(clase 7, arquitectura del dispositivo) y `antena-adaptativa-esp32-web.pdf`
(clase 7, servidor web sobre el propio ESP32).

---

## Clase 10 — Firmware de producción: memoria, robustez, energía y actualización remota

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `ota-nbiot-restringido.pdf` | Mahfoudhi et al. (2022). Over-the-Air Firmware Updates for Constrained NB-IoT Devices. *Sensors* 22(19), 7572. `10.3390/s22197572` | CC BY | **Actualización remota medida** · Coste en tráfico y energía · Dispositivos con recursos limitados |
| `actualizacion-firmware-segura.pdf` | (2020). A Modular End-to-End Framework for Secure Firmware Updates on Embedded Systems. `arXiv:2007.09071` | arXiv | Esquema de dos particiones · Verificación de integridad · Reversión ante fallo |
| `arranque-seguro-atestacion.pdf` | Ling et al. (2021). Secure boot, trusted boot and remote attestation for ARM TrustZone-based IoT Nodes. *J. Syst. Archit.* 119, 102240. `10.1016/j.sysarc.2021.102240` | Copia de repositorio | Arranque seguro · Firma del binario · Cadena de confianza |
| `medicion-consumo-embebidos.pdf` | Guo et al. (2021). A Survey of Energy Consumption Measurement in Embedded Systems. *IEEE Access* 9, 60516-60530. `10.1109/ACCESS.2021.3074070` | CC BY | **Cómo se mide el consumo** · Cálculo de autonomía · Sueño ligero y profundo |
| `vulnerabilidades-firmware-iot.pdf` | Bakhshi et al. (2024). A Review of IoT Firmware Vulnerabilities and Auditing Techniques. *Sensors* 24(2), 708. `10.3390/s24020708` | CC BY | Superficie de exposición · Almacenamiento de credenciales · Cifrado de Flash |

---

## Clase 11 — Firmware compilado y runtime interpretado. Agentes de IA

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `warduino-webassembly.pdf` | Lauwaerts et al. (2024). WARDuino: An embedded WebAssembly virtual machine. *J. Comput. Lang.* 79, 101268. `10.1016/j.cola.2024.101268` | Copia de repositorio | **Runtime interpretado sobre microcontrolador** · Coste frente al binario compilado · Depuración remota |
| `webassembly-embebidos.pdf` | Wallentowitz et al. (2022). Potential of WebAssembly for Embedded Systems. *MECO 2022*, 1-4. `10.1109/MECO55406.2022.9797106` | Copia de autor | Criterios de aplicación · Comparación de rendimiento y memoria |
| `femto-contenedores.pdf` | Zandberg et al. (2022). Femto-Containers: Lightweight Virtualization and Fault Isolation for Small Software Functions on Low-Power IoT Microcontrollers. *Middleware '22*, 161-173. `10.1145/3528535.3565242` | arXiv | Aislamiento de fallos · Actualizar comportamiento sin regrabar · Perfiles de riesgo |
| `webassembly-ciberfisico.pdf` | Van Kenhove et al. (2025). Cyber-Physical WebAssembly: Secure Hardware Interfaces and Pluggable Drivers. *NOMS 2025*, 1-7. `10.1109/NOMS57970.2025.11073737` | Copia de repositorio | Acceso al hardware desde el runtime · Drivers intercambiables |
| `calidad-codigo-generado-ia.pdf` | (2023). Evaluating the Code Quality of AI-Assisted Code Generation Tools: An Empirical Study on GitHub Copilot, Amazon CodeWhisperer and ChatGPT. `arXiv:2304.10778` | CC BY | **Modos de fallo del código generado** · Procedimiento de verificación · Qué revisar siempre |

También aplicables, ya descargados en otra clase: `embedagent-llm-embebidos.pdf`
y `llm-programacion-microcontroladores.pdf` (clase 1, ambos miden modelos de
lenguaje sobre desarrollo embebido real) y `lenguajes-esp32-rendimiento.pdf`
(clase 2, MicroPython frente a C/C++ medido sobre ESP32).

---

## Clase 12 — TinyML y Edge AI: inferencia en microcontroladores

| Archivo | Referencia | Licencia | Temas que sostiene |
|---|---|---|---|
| `cuantizacion-despliegue-microcontroladores.pdf` | Novac et al. (2021). Quantization and Deployment of Deep Neural Networks on Microcontrollers. *Sensors* 21(9), 2984. `10.3390/s21092984` | CC BY | **Cuantización a ocho bits** · Relación entre exactitud, tamaño y tiempo · Flujo de despliegue |
| `revision-tinyml-aprendizaje.pdf` | Capogrosso et al. (2024). A Machine Learning-Oriented Survey on Tiny Machine Learning. *IEEE Access* 12, 23406-23426. `10.1109/ACCESS.2024.3365349` | CC BY | Delimitación de términos · Poda y destilación · Panorámica de herramientas |
| `benchmark-tinyml.pdf` | Banbury et al. (2020). Benchmarking TinyML Systems: Challenges and Direction. `arXiv:2003.04821` | arXiv | **Métricas de evaluación** · Tiempo de inferencia y memoria de trabajo · Por qué la exactitud sola no basta |
| `tinyml-inferencia-aplicaciones.pdf` | Heydari & Mahmoud (2025). Tiny Machine Learning and On-Device Inference: A Survey of Applications, Challenges, and Future Directions. *Sensors* 25(10), 3191. `10.3390/s25103191` | CC BY | Casos de aplicación · Criterios de aplicabilidad · Selección de hardware |
| `deteccion-anomalias-tinyml.pdf` | Antonini et al. (2023). An Adaptable and Unsupervised TinyML Anomaly Detection System for Extreme Industrial Environments. *Sensors* 23(4), 2344. `10.3390/s23042344` | CC BY | **Detección de anomalías y mantenimiento predictivo** · Variación de la distribución en el tiempo · Reentrenamiento |

---

## Conjunto cerrado

Las doce sesiones tienen sus artículos: cinco cada una, seis en la 2, la 3 y la
6, cuatro en la 1. Sesenta y dos en total. No quedan descargas pendientes.

Se descartaron los candidatos que las editoriales solo sirven a un navegador.
Uno se descartó por antigüedad: *Vulnerabilities and Limitations of MQTT
Protocol Used between IoT Devices* (Applied Sciences, 2019). En materia de
seguridad de protocolo, un análisis anterior a la adopción de MQTT 5.0 describe
un estado que ya no es el vigente.

**Desequilibrio conocido en la clase 9.** El servidor web embebido es materia de
práctica de ingeniería, no de literatura revisada por pares: las búsquedas no
devuelven trabajos que lo midan o lo evalúen. Por eso cuatro de los cinco
artículos de esa clase sostienen el Tema B —aprovisionamiento, identidad y
requisitos de producto— y el Tema A se apoya sobre todo en la documentación de
Espressif y en los dos artículos de la clase 7 que sí implementan un servidor
sobre el ESP32.

---

## Limitación conocida

**MDPI y varias editoriales bloquean la descarga automatizada** desde su propio
sitio (responden 403 a cualquier cliente que no sea un navegador). Los
artículos de *Sensors* y *Micromachines* de esta lista se obtuvieron por su
copia depositada en Europe PMC. Los de revistas MDPI **no depositadas en PMC**
—*Electronics*, *Telecom*, *Future Internet*, *Computers*, *Applied
Sciences*— hay que descargarlos a mano. Lo mismo ocurre con ScienceDirect,
ACM DL y eScholarship.

**Verificar siempre el título que imprime el descargador.** Un DOI mal
transcrito no falla: descarga un artículo válido y ajeno. Ya ocurrió una vez
en este proyecto —se guardó un artículo de redes ópticas como si fuera el
benchmark de FreeRTOS— y solo se detectó al abrir el archivo. Por eso
`get-paper.py` contrasta ahora el PDF contra los metadatos de Crossref y
muestra en pantalla el título de lo que ha guardado.
