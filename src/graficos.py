"""
PixelForge MathEngine 2D v1.0
Modulo: graficos.py

.
"""

import os

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAY_MATPLOTLIB = True
except Exception:
    HAY_MATPLOTLIB = False

from matrices import formatear

CARPETA_SALIDA = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "salidas")


def _cerrar(puntos):
    """Repite el primer vertice al final para dibujar el poligono cerrado."""
    return puntos + [puntos[0]] if len(puntos) > 2 else puntos


def graficar(figura_original, figura_transformada=None,
             titulo="MathEngine 2D", nombre_archivo="figura.png"):
    """
    Dibuja la figura original y, si se entrega, la transformada.
    Devuelve la ruta del archivo generado, o None si no hay matplotlib.
    """
    if not HAY_MATPLOTLIB:
        return None

    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    ruta = os.path.join(CARPETA_SALIDA, nombre_archivo)

    fig, ax = plt.subplots(figsize=(6, 6))

    p0 = _cerrar(figura_original.vertices())
    ax.plot([p[0] for p in p0], [p[1] for p in p0], "o-", linewidth=2,
            label=f"{figura_original.nombre} (original)")

    if figura_transformada is not None:
        p1 = _cerrar(figura_transformada.vertices())
        ax.plot([p[0] for p in p1], [p[1] for p in p1], "s--", linewidth=2,
                label=f"{figura_transformada.nombre} (transformada)")

    ax.axhline(0, linewidth=0.8, color="gray")
    ax.axvline(0, linewidth=0.8, color="gray")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.set_title(titulo)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(ruta, dpi=120)
    plt.close(fig)
    return ruta


def grafico_texto(figura, ancho=41, alto=21):
    """Grafico ASCII de respaldo cuando matplotlib no esta disponible."""
    puntos = figura.vertices()
    if not puntos:
        return ""
    escala = max(max(abs(p[0]) for p in puntos),
                 max(abs(p[1]) for p in puntos), 1.0)

    cx, cy = ancho // 2, alto // 2
    lienzo = [[" "] * ancho for _ in range(alto)]
    for i in range(ancho):
        lienzo[cy][i] = "-"
    for i in range(alto):
        lienzo[i][cx] = "|"
    lienzo[cy][cx] = "+"

    for k, (x, y) in enumerate(puntos):
        col = cx + int(round(x / escala * (ancho // 2 - 1)))
        fil = cy - int(round(y / escala * (alto // 2 - 1)))
        if 0 <= fil < alto and 0 <= col < ancho:
            lienzo[fil][col] = str((k + 1) % 10)

    pie = f"  (1 celda ~ {formatear(escala / (ancho // 2 - 1))} unidades)"
    return "\n".join("".join(f) for f in lienzo) + "\n" + pie