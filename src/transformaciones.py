"""
PixelForge MathEngine 2D v1.0
Modulo: transformaciones.py

ACTIVIDAD #2: Transformaciones geometricas.

Requisito de la consigna: el motor debe permitir traslacion, rotacion,
escalamiento y reflexion, mostrando la figura original, la matriz utilizada,
los calculos realizados y la figura transformada; ademas debe permitir aplicar
multiples transformaciones de manera consecutiva.

DECISION DE DISENO CENTRAL
--------------------------
De las cuatro transformaciones solicitadas, TRES son lineales y se aplican
como PRODUCTO de matrices:

        A' = M_{2x2} * A_{2xn}

mientras que la TRASLACION no es lineal. No existe ninguna matriz M de 2x2
que traslade la figura, porque toda transformacion lineal deja fijo el origen
(M * O = O). Por eso la traslacion se implementa como SUMA de matrices:

        A' = A + T,   con T en M_{2 x n}(R) y todas sus columnas iguales a
                      la matriz columna (tx, ty)^t

Ambas operaciones (producto y suma) son exactamente las estudiadas en la
Semana 3, de modo que no se recurre a coordenadas homogeneas.

ORDEN DE APLICACION
-------------------
Como A*B != B*A, el orden en que se aplican las transformaciones consecutivas
modifica el resultado. El motor respeta el orden indicado por el usuario y lo
deja registrado.
"""

import math

from matrices import Matriz, formatear, es_cero
from figuras import Figura


# ----------------------------------------------------------------------
# Matrices de transformacion
# ----------------------------------------------------------------------
def matriz_rotacion(grados):
    """
    R(theta) = | cos(theta)  -sen(theta) |
               | sen(theta)   cos(theta) |

    Rotacion en sentido antihorario alrededor del origen.
    """
    t = math.radians(grados)
    return Matriz([[math.cos(t), -math.sin(t)],
                   [math.sin(t),  math.cos(t)]])


def matriz_escalamiento(sx, sy=None):
    """
    S = | sx   0 |     Es una matriz diagonal.
        |  0  sy |     Si sy se omite, el escalamiento es uniforme.
    """
    if sy is None:
        sy = sx
    if es_cero(sx) or es_cero(sy):
        raise ValueError(
            "Un factor de escala igual a 0 colapsa la figura sobre un eje "
            "y la transformacion deja de ser reversible.")
    return Matriz([[float(sx), 0.0],
                   [0.0, float(sy)]])


EJES_REFLEXION = {
    "x":      ("eje X",           [[1, 0], [0, -1]]),
    "y":      ("eje Y",           [[-1, 0], [0, 1]]),
    "origen": ("origen",          [[-1, 0], [0, -1]]),
    "y=x":    ("recta y = x",     [[0, 1], [1, 0]]),
    "y=-x":   ("recta y = -x",    [[0, -1], [-1, 0]]),
}


def matriz_reflexion(eje):
    """Matriz de reflexion respecto a: x, y, origen, y=x o y=-x."""
    clave = str(eje).strip().lower().replace(" ", "")
    if clave not in EJES_REFLEXION:
        raise KeyError(
            f"Eje '{eje}' no valido. Opciones: {', '.join(EJES_REFLEXION)}")
    return Matriz(EJES_REFLEXION[clave][1])


def nombre_eje(eje):
    return EJES_REFLEXION[str(eje).strip().lower().replace(" ", "")][0]


def matriz_traslacion(tx, ty, n):
    """
    T en M_{2 x n}(R) con todas sus columnas iguales a (tx, ty)^t.
    Se construye del ancho de la figura para poder sumarla.
    """
    return Matriz([[float(tx)] * n,
                   [float(ty)] * n])


# ----------------------------------------------------------------------
# Resultado de una transformacion
# ----------------------------------------------------------------------
class Resultado:
    """
    Empaqueta todo lo que la consigna exige mostrar de una transformacion.
    La Actividad #4 consumira estos objetos para armar el historial.
    """

    def __init__(self, descripcion, operacion, matriz_usada,
                 figura_antes, figura_despues, calculos):
        self.descripcion = descripcion      # "Rotacion de 45 grados"
        self.operacion = operacion          # "producto" | "suma" | "compuesta"
        self.matriz_usada = matriz_usada
        self.figura_antes = figura_antes
        self.figura_despues = figura_despues
        self.calculos = calculos            # lista de lineas de texto

    def informe(self):
        """Texto completo con los cinco elementos que pide la consigna."""
        L = []
        L.append(f"Transformacion: {self.descripcion}")
        L.append("")
        L.append("Figura original:")
        L.append(str(self.figura_antes.matriz))
        L.append(self.figura_antes.texto_vertices())
        L.append("")
        L.append("Matriz utilizada:")
        L.append(str(self.matriz_usada))
        L.append("Clasificacion: " + ", ".join(self.matriz_usada.clasificacion()))
        L.append("")
        L.append("Calculos realizados:")
        L.extend(self.calculos)
        L.append("")
        L.append("Figura transformada:")
        L.append(str(self.figura_despues.matriz))
        L.append(self.figura_despues.texto_vertices())
        return "\n".join(L)


# ----------------------------------------------------------------------
# Aplicacion de las transformaciones
# ----------------------------------------------------------------------
def aplicar_lineal(figura, M, descripcion):
    """A' = M * A. Sirve para rotacion, escalamiento y reflexion."""
    A = figura.matriz
    A_nueva = M.producto(A)
    calculos = [f"A' = M * A   ({M.m}x{M.n}) * ({A.m}x{A.n}) = ({A_nueva.m}x{A_nueva.n})"]
    calculos += M.detalle_producto(A)
    return Resultado(descripcion, "producto", M, figura,
                     Figura.desde_matriz(figura.nombre, A_nueva), calculos)


def trasladar(figura, tx, ty):
    """A' = A + T."""
    A = figura.matriz
    T = matriz_traslacion(tx, ty, A.n)
    A_nueva = A.suma(T)
    calculos = [f"A' = A + T   (suma de matrices de {A.m}x{A.n})"]
    for j in range(A.n):
        calculos.append(
            f"  P{j + 1}' = ({formatear(A.datos[0][j])} + {formatear(tx)}, "
            f"{formatear(A.datos[1][j])} + {formatear(ty)}) = "
            f"({formatear(A_nueva.datos[0][j])}, {formatear(A_nueva.datos[1][j])})")
    return Resultado(f"Traslacion por el vector ({formatear(tx)}, {formatear(ty)})",
                     "suma", T, figura,
                     Figura.desde_matriz(figura.nombre, A_nueva), calculos)


def rotar(figura, grados, centro=None):
    """Rotacion de la figura. Si centro es None, se rota alrededor del origen."""
    M = matriz_rotacion(grados)
    if centro is None:
        return aplicar_lineal(figura, M, f"Rotacion de {formatear(grados)} grados")
    return _respecto_a_centro(
        figura, M, centro,
        f"Rotacion de {formatear(grados)} grados respecto a "
        f"({formatear(centro[0])}, {formatear(centro[1])})")


def escalar(figura, sx, sy=None, centro=None):
    """Escalamiento de la figura. Si centro es None, se escala desde el origen."""
    M = matriz_escalamiento(sx, sy)
    etiqueta = formatear(sx) if sy is None else f"({formatear(sx)}, {formatear(sy)})"
    if centro is None:
        return aplicar_lineal(figura, M, f"Escalamiento de factor {etiqueta}")
    return _respecto_a_centro(
        figura, M, centro,
        f"Escalamiento de factor {etiqueta} respecto a "
        f"({formatear(centro[0])}, {formatear(centro[1])})")


def reflejar(figura, eje):
    """Reflexion respecto a x, y, origen, y=x o y=-x."""
    M = matriz_reflexion(eje)
    return aplicar_lineal(figura, M, f"Reflexion respecto al {nombre_eje(eje)}")


def _respecto_a_centro(figura, M, centro, descripcion):
    """
    Toda transformacion lineal fija el origen. Para rotar o escalar respecto
    a un punto c distinto del origen se compone:

        1) trasladar la figura por -c   (llevar c al origen)
        2) aplicar M
        3) trasladar de vuelta por +c

    Es decir:  A' = M * (A - C) + C
    """
    cx, cy = float(centro[0]), float(centro[1])
    paso1 = trasladar(figura, -cx, -cy)
    paso2 = aplicar_lineal(paso1.figura_despues, M, descripcion)
    paso3 = trasladar(paso2.figura_despues, cx, cy)

    calculos = [f"A' = M * (A - C) + C   con C = ({formatear(cx)}, {formatear(cy)})",
                "",
                f"Paso 1 - trasladar por (-{formatear(cx)}, -{formatear(cy)}):"]
    calculos += paso1.calculos[1:]
    calculos += ["", "Paso 2 - aplicar la matriz M:"]
    calculos += paso2.calculos[1:]
    calculos += ["", f"Paso 3 - trasladar por ({formatear(cx)}, {formatear(cy)}):"]
    calculos += paso3.calculos[1:]

    return Resultado(descripcion, "compuesta", M, figura,
                     paso3.figura_despues, calculos)


# ----------------------------------------------------------------------
# Transformaciones consecutivas
# ----------------------------------------------------------------------
def aplicar_secuencia(figura, operaciones):
    """
    Aplica varias transformaciones seguidas, en el orden indicado.

    operaciones: lista de tuplas, por ejemplo
        [("rotar", 30), ("escalar", 1.5), ("trasladar", (3, 1))]

    Devuelve (figura_final, lista_de_Resultado).
    """
    actual = figura
    resultados = []
    for op in operaciones:
        clave = str(op[0]).lower()
        if clave == "rotar":
            r = rotar(actual, op[1])
        elif clave == "escalar":
            arg = op[1]
            r = escalar(actual, *arg) if isinstance(arg, (tuple, list)) \
                else escalar(actual, arg)
        elif clave == "reflejar":
            r = reflejar(actual, op[1])
        elif clave == "trasladar":
            tx, ty = op[1]
            r = trasladar(actual, tx, ty)
        else:
            raise KeyError(f"Operacion desconocida: {op[0]}")
        resultados.append(r)
        actual = r.figura_despues
    return actual, resultados


def matriz_compuesta(matrices):
    """
    Para transformaciones LINEALES aplicadas en el orden M1, M2, ..., Mk, la
    matriz equivalente es el producto acumulado

        M = Mk * ... * M2 * M1

    La primera en aplicarse queda a la derecha, por la asociatividad del
    producto de matrices. Permite precalcular una sola matriz en lugar de
    recorrer la figura k veces.

    ATENCION: no es valido incluir traslaciones, porque no son lineales.
    """
    M = Matriz.identidad(2)
    for Mi in matrices:
        M = Mi.producto(M)
    return M