"""
PixelForge MathEngine 2D v1.0
Modulo: transformaciones.py

ACTIVIDAD #2: Transformaciones geometricas.

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
# ======================================================================
# COORDENADAS HOMOGENEAS (matrices de 3 x 3)
# ======================================================================
# Este bloque es ADITIVO: no reemplaza nada de lo anterior. Ofrece una
# segunda via para aplicar las mismas transformaciones.
#
# FUNDAMENTO
# ----------
# En la forma cartesiana, la traslacion no puede expresarse como producto
# porque toda matriz cumple M * O = O: las transformaciones lineales dejan
# fijo el origen.
#
# Las coordenadas homogeneas resuelven ese problema agregando una tercera
# componente. Cada punto (x, y) se representa como (x, y, 1), y la figura
# pasa de ser una matriz de 2 x n a una de 3 x n:
#
#           | x1  x2  ...  xn |
#     A_h = | y1  y2  ...  yn |
#           |  1   1  ...   1 |
#
# Con esa tercera fila, la traslacion SI se escribe como producto:
#
#     | 1  0  tx |   | x |     | x + tx |
#     | 0  1  ty | * | y |  =  | y + ty |
#     | 0  0   1 |   | 1 |     |    1   |
#
# La fila (0, 0, 1) es la que mantiene la componente w igual a 1 despues de
# cualquier transformacion afin.
#
# CONSECUENCIA PRACTICA
# ---------------------
# Como las cuatro transformaciones son ahora productos, una secuencia
# completa (incluyendo traslaciones) puede condensarse en UNA sola matriz
# de 3x3, en lugar de recorrer la figura una vez por transformacion. Es lo
# que hacen los motores graficos reales.
# ======================================================================

def a_homogenea(M):
    """
    Convierte una matriz lineal de 2x2 en su equivalente homogenea de 3x3:

        | a  b |         | a  b  0 |
        | c  d |   -->   | c  d  0 |
                         | 0  0  1 |

    La tercera columna es 0 porque la transformacion no traslada, y la
    tercera fila (0, 0, 1) preserva la componente w.
    """
    if M.tamano != (2, 2):
        raise ValueError(f"Se esperaba una matriz de 2x2; se recibio {M.m}x{M.n}.")
    return Matriz([
        [M.datos[0][0], M.datos[0][1], 0.0],
        [M.datos[1][0], M.datos[1][1], 0.0],
        [0.0,           0.0,           1.0],
    ])


def matriz_rotacion_h(grados):
    """Rotacion en coordenadas homogeneas."""
    return a_homogenea(matriz_rotacion(grados))


def matriz_escalamiento_h(sx, sy=None):
    """Escalamiento en coordenadas homogeneas."""
    return a_homogenea(matriz_escalamiento(sx, sy))


def matriz_reflexion_h(eje):
    """Reflexion en coordenadas homogeneas."""
    return a_homogenea(matriz_reflexion(eje))


def matriz_traslacion_h(tx, ty):
    """
    Traslacion en coordenadas homogeneas:

        T = | 1  0  tx |
            | 0  1  ty |
            | 0  0   1 |

    A diferencia de la version cartesiana, esta matriz es de 3x3 y NO
    depende de la cantidad de vertices de la figura: es siempre la misma.
    """
    return Matriz([[1.0, 0.0, float(tx)],
                   [0.0, 1.0, float(ty)],
                   [0.0, 0.0, 1.0]])


def matriz_transformacion_h(operacion):
    """
    Construye la matriz homogenea 3x3 correspondiente a una operacion.

    operacion es una tupla como ("rotar", 30) o ("trasladar", (3, 1)),
    con el mismo formato que usa aplicar_secuencia.

    Devuelve (matriz, descripcion).
    """
    clave = str(operacion[0]).lower()
    if clave == "rotar":
        return (matriz_rotacion_h(operacion[1]),
                f"Rotacion de {formatear(operacion[1])} grados")
    if clave == "escalar":
        arg = operacion[1]
        if isinstance(arg, (tuple, list)):
            return (matriz_escalamiento_h(*arg),
                    f"Escalamiento de factor ({formatear(arg[0])}, {formatear(arg[1])})")
        return (matriz_escalamiento_h(arg), f"Escalamiento de factor {formatear(arg)}")
    if clave == "reflejar":
        return (matriz_reflexion_h(operacion[1]),
                f"Reflexion respecto al {nombre_eje(operacion[1])}")
    if clave == "trasladar":
        tx, ty = operacion[1]
        return (matriz_traslacion_h(tx, ty),
                f"Traslacion por el vector ({formatear(tx)}, {formatear(ty)})")
    raise KeyError(f"Operacion desconocida: {operacion[0]}")


def matriz_compuesta_h(matrices):
    """
    Producto acumulado de matrices homogeneas 3x3.

        M = Mk * ... * M2 * M1

    La primera transformacion aplicada queda a la DERECHA, igual que en la
    version cartesiana, por la asociatividad del producto.

    A diferencia de matriz_compuesta(), esta version SI admite traslaciones,
    porque en coordenadas homogeneas tambien son productos.
    """
    M = Matriz.identidad(3)
    for Mi in matrices:
        if Mi.tamano != (3, 3):
            raise ValueError("Todas las matrices deben ser de 3x3.")
        M = Mi.producto(M)
    return M


def aplicar_homogenea(figura, H, descripcion):
    """
    Aplica una transformacion homogenea a la figura:  A_h' = H * A_h

    La figura se convierte a 3 x n, se multiplica por la matriz de 3x3 y el
    resultado se convierte de vuelta a coordenadas cartesianas.
    """
    if H.tamano != (3, 3):
        raise ValueError(f"Se esperaba una matriz de 3x3; se recibio {H.m}x{H.n}.")

    A_h = figura.matriz_homogenea()
    A_nueva_h = H.producto(A_h)

    calculos = [
        f"A_h' = H * A_h   ({H.m}x{H.n}) * ({A_h.m}x{A_h.n}) = "
        f"({A_nueva_h.m}x{A_nueva_h.n})",
        "",
        "Figura en coordenadas homogeneas (se agrega la fila de unos):",
    ]
    calculos += ["  " + linea for linea in str(A_h).split("\n")]
    calculos += ["", "Desarrollo del producto:"]
    calculos += H.detalle_producto(A_h)
    calculos += ["", "Resultado homogeneo (la tercera fila se mantiene en 1):"]
    calculos += ["  " + linea for linea in str(A_nueva_h).split("\n")]

    return Resultado(descripcion, "homogenea", H, figura,
                     Figura.desde_matriz(figura.nombre, A_nueva_h), calculos)


def aplicar_secuencia_homogenea(figura, operaciones):
    """
    Aplica varias transformaciones condensandolas en UNA sola matriz de 3x3.

    A diferencia de aplicar_secuencia(), que recorre la figura una vez por
    transformacion, aqui se calcula primero la matriz compuesta y luego se
    aplica una unica vez. El resultado es el mismo.

    Devuelve (figura_final, matriz_compuesta, resultado, detalle_pasos)
    donde detalle_pasos lista cada matriz individual con su descripcion.
    """
    if not operaciones:
        raise ValueError("Debe indicar al menos una transformacion.")

    matrices = []
    detalle_pasos = []
    for op in operaciones:
        H, desc = matriz_transformacion_h(op)
        matrices.append(H)
        detalle_pasos.append((desc, H))

    H_total = matriz_compuesta_h(matrices)
    descripcion = "Secuencia homogenea: " + " -> ".join(d for d, _ in detalle_pasos)
    resultado = aplicar_homogenea(figura, H_total, descripcion)

    return resultado.figura_despues, H_total, resultado, detalle_pasos