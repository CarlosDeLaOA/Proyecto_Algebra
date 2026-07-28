"""
PixelForge MathEngine 2D v1.0
Modulo: analisis.py

ACTIVIDAD #3: Analisis matematico del escenario.

Requisito de la consigna: analizar espacios vectoriales y subespacios,
verificar independencia lineal, determinar bases y dimension, detectar
informacion redundante e interpretar geometricamente los resultados.

Todo el modulo se apoya en UN SOLO algoritmo escrito por el equipo: la
reduccion de Gauss-Jordan. De su forma escalonada reducida se derivan el
rango, la independencia lineal, la base, la dimension y la redundancia.

No se utiliza numpy.linalg.matrix_rank, numpy.linalg.solve ni equivalentes.
"""

from matrices import Matriz, es_cero, formatear


# ----------------------------------------------------------------------
# Algoritmo base: reduccion de Gauss-Jordan
# ----------------------------------------------------------------------
def gauss_jordan(A, registrar_pasos=True):
    """
    Lleva A a su forma escalonada REDUCIDA por filas.

    Devuelve (R, pivotes, pasos):
        R       : matriz escalonada reducida
        pivotes : indices de columna (0-based) que contienen pivote
        pasos   : descripcion de las operaciones elementales aplicadas

    Operaciones elementales utilizadas:
        F_i <-> F_k          intercambio
        F_i <- (1/p) F_i     normalizacion del pivote
        F_k <- F_k - c F_i   eliminacion
    """
    R = A.copia()
    pasos = []
    pivotes = []
    fila_actual = 0

    for col in range(R.n):
        if fila_actual >= R.m:
            break

        # 1) Elegir como pivote la entrada de mayor valor absoluto de la
        #    columna. Reduce el error numerico acumulado.
        mejor = fila_actual
        for i in range(fila_actual + 1, R.m):
            if abs(R.datos[i][col]) > abs(R.datos[mejor][col]):
                mejor = i

        if es_cero(R.datos[mejor][col]):
            continue  # columna sin pivote -> variable libre

        # 2) Intercambio de filas
        if mejor != fila_actual:
            R.datos[fila_actual], R.datos[mejor] = R.datos[mejor], R.datos[fila_actual]
            if registrar_pasos:
                pasos.append(f"F{fila_actual + 1} <-> F{mejor + 1}")

        # 3) Normalizar el pivote a 1
        p = R.datos[fila_actual][col]
        if not es_cero(p - 1.0):
            R.datos[fila_actual] = [x / p for x in R.datos[fila_actual]]
            if registrar_pasos:
                pasos.append(f"F{fila_actual + 1} <- (1/{formatear(p)}) F{fila_actual + 1}")

        # 4) Anular el resto de la columna, arriba y abajo
        for i in range(R.m):
            if i == fila_actual:
                continue
            c = R.datos[i][col]
            if es_cero(c):
                continue
            R.datos[i] = [R.datos[i][k] - c * R.datos[fila_actual][k]
                          for k in range(R.n)]
            if registrar_pasos:
                pasos.append(f"F{i + 1} <- F{i + 1} - ({formatear(c)}) F{fila_actual + 1}")

        pivotes.append(col)
        fila_actual += 1

    # Limpieza de residuos de punto flotante
    for i in range(R.m):
        for j in range(R.n):
            if es_cero(R.datos[i][j]):
                R.datos[i][j] = 0.0

    return R, pivotes, pasos


def rango(A):
    """Rango de A = cantidad de pivotes de su forma escalonada reducida."""
    _, pivotes, _ = gauss_jordan(A, registrar_pasos=False)
    return len(pivotes)


# ----------------------------------------------------------------------
# Independencia lineal, base y dimension
# ----------------------------------------------------------------------
def matriz_de_vectores(vectores):
    """Arma la matriz cuyas COLUMNAS son los vectores dados."""
    if not vectores:
        raise ValueError("Debe indicar al menos un vector.")
    dim = len(vectores[0])
    for v in vectores:
        if len(v) != dim:
            raise ValueError(
                "Todos los vectores deben tener la misma cantidad de componentes.")
    return Matriz([[float(v[i]) for v in vectores] for i in range(dim)])


def analizar_conjunto(vectores, etiquetas=None):
    """
    Analiza un conjunto de vectores colocados como columnas de una matriz.

    Devuelve un diccionario con matriz, escalonada, pasos, pivotes, libres,
    rango, dimension, independiente, base, redundantes y combinaciones.
    """
    if etiquetas is None:
        etiquetas = [f"v{i + 1}" for i in range(len(vectores))]

    A = matriz_de_vectores(vectores)
    R, pivotes, pasos = gauss_jordan(A)
    libres = [j for j in range(A.n) if j not in pivotes]

    # Cada columna libre se expresa como combinacion lineal de las columnas
    # pivote: sus entradas en la escalonada reducida SON los coeficientes.
    combinaciones = {}
    for j in libres:
        terminos = []
        for fila, col_piv in enumerate(pivotes):
            coef = R.datos[fila][j]
            if not es_cero(coef):
                terminos.append(f"({formatear(coef)})*{etiquetas[col_piv]}")
        combinaciones[etiquetas[j]] = " + ".join(terminos) if terminos else "0"

    return {
        "matriz": A,
        "escalonada": R,
        "pasos": pasos,
        "pivotes": pivotes,
        "libres": libres,
        "rango": len(pivotes),
        "dimension": len(pivotes),
        "independiente": len(pivotes) == A.n,
        "base": [vectores[j] for j in pivotes],
        "etiquetas_base": [etiquetas[j] for j in pivotes],
        "redundantes": [etiquetas[j] for j in libres],
        "combinaciones": combinaciones,
        "etiquetas": etiquetas,
    }


def informe_conjunto(vectores, etiquetas=None):
    """Version en texto del analisis, lista para imprimir en la interfaz."""
    r = analizar_conjunto(vectores, etiquetas)
    L = []
    L.append("Matriz cuyas columnas son los vectores analizados:")
    L.append(str(r["matriz"]))
    L.append("")
    L.append("Reduccion de Gauss-Jordan:")
    if r["pasos"]:
        for p in r["pasos"]:
            L.append(f"  {p}")
    else:
        L.append("  (la matriz ya estaba en forma escalonada reducida)")
    L.append("")
    L.append("Forma escalonada reducida:")
    L.append(str(r["escalonada"]))
    L.append("")
    etq = ", ".join(r["etiquetas_base"]) if r["etiquetas_base"] else "ninguna"
    L.append(f"Rango = {r['rango']}   (columnas pivote: {etq})")
    L.append("")

    if r["independiente"]:
        L.append("El conjunto es LINEALMENTE INDEPENDIENTE:")
        L.append("ningun vector es combinacion lineal de los demas.")
    else:
        L.append("El conjunto es LINEALMENTE DEPENDIENTE.")
        L.append("Vectores que son combinacion lineal de los demas:")
        for nombre, expr in r["combinaciones"].items():
            if expr == "0":
                L.append(f"  {nombre} = 0  (es el vector nulo: siempre es "
                         f"combinacion lineal de cualquier conjunto)")
            else:
                L.append(f"  {nombre} = {expr}")

    L.append("")
    L.append(f"Base encontrada: {{ {', '.join(r['etiquetas_base'])} }}")
    for etiqueta, v in zip(r["etiquetas_base"], r["base"]):
        L.append(f"  {etiqueta} = ({', '.join(formatear(c) for c in v)})")
    L.append(f"Dimension del subespacio generado = {r['dimension']}")
    L.append("")
    L.append("Interpretacion: todo el conjunto puede representarse utilizando")
    L.append(f"unicamente estos {r['dimension']} vector(es).")
    return "\n".join(L)


# ----------------------------------------------------------------------
# Vertices redundantes de una figura
# ----------------------------------------------------------------------
def vertices_redundantes(figura, cerrada=True):
    """
    Detecta vertices que NO aportan informacion a la forma del poligono.

    Criterio: el vertice P_k es redundante si los vectores de arista
        u = P_k - P_{k-1}      y      w = P_{k+1} - P_k
    son linealmente DEPENDIENTES (el rango de la matriz [u  w] es menor
    que 2). En ese caso P_k esta alineado con sus vecinos y se puede
    eliminar sin alterar la figura dibujada.

    ADVERTENCIA CONCEPTUAL
    ----------------------
    Esto NO es lo mismo que analizar la independencia lineal de los vectores
    de POSICION de los vertices. En R^2 cualquier conjunto de 3 o mas
    vectores de posicion es forzosamente dependiente, porque la dimension
    maxima del espacio es 2; ese analisis nunca serviria para optimizar un
    poligono. La redundancia geometrica se mide sobre las ARISTAS.

    Devuelve (indices_redundantes, vertices_optimizados).
    """
    P = figura.vertices()
    n = len(P)
    if n < 3:
        return [], P

    indices = []
    for k in range(n):
        if not cerrada and (k == 0 or k == n - 1):
            continue  # los extremos de una polilinea abierta nunca sobran
        anterior = P[(k - 1) % n]
        siguiente = P[(k + 1) % n]
        u = (P[k][0] - anterior[0], P[k][1] - anterior[1])
        w = (siguiente[0] - P[k][0], siguiente[1] - P[k][1])
        M = Matriz([[u[0], w[0]],
                    [u[1], w[1]]])
        if rango(M) < 2:
            indices.append(k)

    optimizada = [P[k] for k in range(n) if k not in indices]
    return indices, optimizada


def informe_redundancia(figura, cerrada=True):
    """Texto del analisis de redundancia. Devuelve (lineas, optimizada)."""
    indices, optimizada = vertices_redundantes(figura, cerrada)
    L = []
    L.append(f"Objeto analizado: {figura.nombre}")
    L.append(f"Vertices originales: {figura.cantidad_vertices}")
    L.append("")

    if figura.cantidad_vertices < 3:
        L.append("Con menos de 3 vertices no se puede evaluar la colinealidad.")
        return L, optimizada

    if not indices:
        L.append("No se detectaron vertices redundantes: para cada vertice, los")
        L.append("vectores de arista entrante y saliente son linealmente")
        L.append("independientes. La representacion ya es optima.")
        return L, optimizada

    L.append("Vertices redundantes detectados (alineados con sus vecinos):")
    P = figura.vertices()
    for k in indices:
        anterior = P[(k - 1) % len(P)]
        siguiente = P[(k + 1) % len(P)]
        u = (P[k][0] - anterior[0], P[k][1] - anterior[1])
        w = (siguiente[0] - P[k][0], siguiente[1] - P[k][1])
        L.append(f"  P{k + 1} = ({formatear(P[k][0])}, {formatear(P[k][1])})")
        L.append(f"    arista entrante u = ({formatear(u[0])}, {formatear(u[1])})")
        L.append(f"    arista saliente w = ({formatear(w[0])}, {formatear(w[1])})")
        L.append(f"    rango de [u  w] = {rango(Matriz([[u[0], w[0]], [u[1], w[1]]]))} "
                 f"< 2  ->  u y w son linealmente dependientes")
    L.append("")
    L.append(f"El usuario indico {figura.cantidad_vertices} puntos; "
             f"{len(indices)} eran combinacion lineal de sus aristas vecinas.")
    L.append(f"Representacion optimizada: {len(optimizada)} vertices")
    for k, (x, y) in enumerate(optimizada):
        L.append(f"  Q{k + 1} = ({formatear(x)}, {formatear(y)})")
    L.append("")
    L.append("Interpretacion geometrica: la figura dibujada es exactamente la")
    L.append("misma, pero el motor almacena y transforma menos columnas, lo que")
    L.append("reduce el costo de cada producto M * A.")
    return L, optimizada


# ----------------------------------------------------------------------
# Espacios y subespacios vectoriales
# ----------------------------------------------------------------------
def verificar_subespacio_recta(a, b, c, muestra=None):
    """
    Analiza el conjunto  W = { (x, y) en R^2 : a*x + b*y = c }
    (por ejemplo, las posiciones validas del personaje sobre x + y = 10).

    Verifica las tres condiciones de subespacio vectorial:
        1. El vector nulo pertenece a W
        2. Cierre bajo la suma
        3. Cierre bajo el producto por un escalar

    Devuelve (es_subespacio, lineas_de_texto).
    """
    if es_cero(a) and es_cero(b):
        raise ValueError("Si a = b = 0 la condicion no define una recta.")

    L = []
    L.append(f"Conjunto analizado:")
    L.append(f"  W = {{ (x, y) en R^2 : {formatear(a)}x + {formatear(b)}y "
             f"= {formatear(c)} }}")
    L.append("")

    # Dos puntos distintos de W, para construir ejemplos o contraejemplos.
    if es_cero(c):
        # La recta pasa por el origen: se usan multiplos del vector director.
        u = (-b, a)
        v = (-2.0 * b, 2.0 * a)
    elif es_cero(a):                 # recta horizontal  y = c/b
        u, v = (0.0, c / b), (1.0, c / b)
    elif es_cero(b):                 # recta vertical    x = c/a
        u, v = (c / a, 0.0), (c / a, 1.0)
    else:                            # cortes con los ejes
        u, v = (c / a, 0.0), (0.0, c / b)

    def evaluar(p):
        return a * p[0] + b * p[1]

    # ---- Condicion 1: el vector nulo
    cumple_nulo = es_cero(0.0 - c)
    L.append("1) El vector nulo pertenece a W?")
    L.append(f"   {formatear(a)}*0 + {formatear(b)}*0 = 0, "
             f"y se requiere que sea igual a {formatear(c)}.")
    L.append("   -> SI cumple." if cumple_nulo else "   -> NO cumple.")

    # ---- Condicion 2: cierre bajo la suma
    s = (u[0] + v[0], u[1] + v[1])
    cumple_suma = es_cero(evaluar(s) - c)
    L.append("")
    L.append("2) Cierre bajo la suma?")
    L.append(f"   Se toman u = ({formatear(u[0])}, {formatear(u[1])}) y "
             f"v = ({formatear(v[0])}, {formatear(v[1])}), ambos en W.")
    L.append(f"   u + v = ({formatear(s[0])}, {formatear(s[1])})")
    L.append(f"   {formatear(a)}*{formatear(s[0])} + {formatear(b)}*{formatear(s[1])} "
             f"= {formatear(evaluar(s))}")
    L.append("   -> SI cumple." if cumple_suma
             else f"   -> NO cumple, pues {formatear(evaluar(s))} != {formatear(c)}.")

    # ---- Condicion 3: cierre bajo el producto por escalar
    lam = 2.0
    e = (lam * u[0], lam * u[1])
    cumple_escalar = es_cero(evaluar(e) - c)
    L.append("")
    L.append("3) Cierre bajo el producto por un escalar?")
    L.append(f"   Con lambda = {formatear(lam)} y u = "
             f"({formatear(u[0])}, {formatear(u[1])}):")
    L.append(f"   lambda*u = ({formatear(e[0])}, {formatear(e[1])})")
    L.append(f"   {formatear(a)}*{formatear(e[0])} + {formatear(b)}*{formatear(e[1])} "
             f"= {formatear(evaluar(e))}")
    L.append("   -> SI cumple." if cumple_escalar
             else f"   -> NO cumple, pues {formatear(evaluar(e))} != {formatear(c)}.")

    resultado = cumple_nulo and cumple_suma and cumple_escalar
    L.append("")
    if resultado:
        L.append("CONCLUSION: W SI es un subespacio vectorial de R^2.")
        L.append("")
        L.append("Geometricamente es una recta que pasa por el origen. Su")
        L.append("dimension es 1 y una base la forma su vector director.")
        L.append(f"  Base de W: {{ ({formatear(-b)}, {formatear(a)}) }}")
        L.append("  Dimension = 1")
        L.append("")
        L.append("Para el motor: cualquier suma de posiciones validas o cualquier")
        L.append("multiplo de una posicion valida sigue siendo una posicion valida.")
    else:
        L.append("CONCLUSION: W NO es un subespacio vectorial de R^2.")
        L.append("")
        L.append("Geometricamente es una recta que NO pasa por el origen: es la")
        L.append("traslacion de un subespacio, no un subespacio en si mismo.")
        L.append("")
        L.append("Para el motor: el conjunto de posiciones validas es un conjunto")
        L.append("AFIN. Se puede describir como P0 + t*d, pero no se le pueden")
        L.append("aplicar libremente sumas ni escalados sin salirse de el.")
        if not es_cero(c):
            L.append("")
            L.append(f"  Punto base P0 = ({formatear(u[0])}, {formatear(u[1])})")
            L.append(f"  Direccion   d = ({formatear(-b)}, {formatear(a)})")

    if muestra:
        L.append("")
        L.append("Verificacion de posiciones concretas:")
        for p in muestra:
            dentro = es_cero(evaluar(p) - c)
            L.append(f"  ({formatear(p[0])}, {formatear(p[1])}): "
                     f"{formatear(a)}*{formatear(p[0])} + "
                     f"{formatear(b)}*{formatear(p[1])} = {formatear(evaluar(p))}"
                     f"  ->  {'posicion VALIDA' if dentro else 'posicion INVALIDA'}")

    return resultado, L