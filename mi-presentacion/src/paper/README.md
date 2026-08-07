# Artículos de las sesiones

**Los PDF no se versionan en este repositorio.** Son 62 artículos de terceros:
todos de acceso abierto, pero acceso abierto no equivale a permiso de
redistribución, y al menos uno se publicó bajo CC BY-ND, que prohíbe difundir
versiones adaptadas.

Lo que sí está aquí es [`INDICE.md`](INDICE.md), con la referencia completa y el
DOI de cada uno. Con el DOI, cada artículo se descarga de su editorial en su
versión definitiva, que es además la que hay que citar.

Para reconstruir las carpetas `clase-NN/` en una copia local:

```
python3 tools/get-paper.py        # descarga a partir de los DOI del índice
```

Las figuras de las láminas de artículo **no** reproducen las de los artículos.
Se dibujan en `tools/figures/render.py` a partir de las cifras publicadas —los
datos no son objeto de derechos de autor— y llevan el pie «elaboración propia a
partir de las cifras publicadas». Por eso las láminas se ven completas aunque
falten los PDF.
