# Proyecto Algebra Lineal

---

## Descripción

El motor permite representar objetos 2D mediante coordenadas cartesianas, aplicarles transformaciones geométricas, analizar sus propiedades con herramientas de álgebra lineal y reconstruir el historial de modificaciones de cada objeto.

Todas las operaciones matriciales están implementadas desde cero. El proyecto no importa `numpy` en ningún módulo.

---

## Ejecución

```bash
cd src
python3 main.py
```

Requiere Python 3.8 o superior. `matplotlib` es opcional, solo para los gráficos:

```bash
pip install matplotlib
```

Sin matplotlib el programa funciona igual y dibuja en modo texto.

---

## Estructura

```
mathengine2d/
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   ├── matrices.py          núcleo de álgebra matricial
│   ├── figuras.py           Actividad #1
│   ├── transformaciones.py  Actividad #2
│   ├── analisis.py          Actividad #3
│   ├── historial.py         Actividad #4
│   ├── graficos.py          representación gráfica
│   └── main.py              interfaz de consola
├── docs/
│   ├── pseudocodigos.md
│   ├── informe_tecnico.md
│   └── bitacora_ia.md
└── salidas/                 imágenes generadas (ignorada por Git)
```

---

## Funcionalidades

**Actividad #1 — Representación.** Los objetos se construyen indicando sus coordenadas cartesianas o ingresando directamente su matriz. Se almacenan como matrices de 2×n, con un vértice por columna.

**Actividad #2 — Transformaciones.** Traslación, rotación, escalamiento y reflexión, individuales o consecutivas. El programa muestra la figura original, la matriz utilizada, los cálculos y la figura transformada. Rotación y escalamiento admiten un centro distinto del origen.

**Actividad #3 — Análisis.** Verificación de subespacios vectoriales, independencia lineal, bases y dimensión, y detección de vértices redundantes.

**Actividad #4 — Historial.** Cada objeto conserva el registro de sus transformaciones y permite reconstruir cualquier estado anterior o deshacer.

---

## Integrantes

Samanta Toruño Sequeira
Camila Morales Solano
Carlos De La O Arce

## Fuentes

Paez, C. (2013). *Matrices y Sistemas* (1.ª ed.).