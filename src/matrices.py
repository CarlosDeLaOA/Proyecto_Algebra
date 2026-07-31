"""
PixelForge MathEngine 2D v1.0
Modulo: matrices.py

"""

TOLERANCIA = 1e-9


def es_cero(x):
    """Comparacion contra 0 con tolerancia, para evitar residuos como 1e-17."""
    return abs(x) < TOLERANCIA


def formatear(x):
    """Formato de impresion de un numero real."""
    if es_cero(x):
        x = 0.0
    if abs(x - round(x)) < TOLERANCIA:
        return str(int(round(x)))
    return f"{x:.4f}".rstrip("0").rstrip(".")


class Matriz:
    """Matriz real de tamano m x n, almacenada como lista de filas."""

    # ------------------------------------------------------------------
    # Construccion
    # ------------------------------------------------------------------
    def __init__(self, datos):
        if not isinstance(datos, (list, tuple)) or len(datos) == 0:
            raise ValueError("Una matriz debe construirse a partir de una lista de filas.")
        if not isinstance(datos[0], (list, tuple)) or len(datos[0]) == 0:
            raise ValueError("Cada fila debe ser una lista con al menos un elemento.")

        n = len(datos[0])
        for k, fila in enumerate(datos):
            if len(fila) != n:
                raise ValueError(
                    f"La fila {k + 1} tiene {len(fila)} elementos, pero se esperaban {n}. "
                    "Todas las filas deben tener la misma cantidad de columnas.")
            for x in fila:
                if isinstance(x, bool) or not isinstance(x, (int, float)):
                    raise TypeError(f"El valor {x!r} no es un numero real valido.")

        self.datos = [[float(x) for x in fila] for fila in datos]
        self.m = len(datos)   # cantidad de filas
        self.n = n            # cantidad de columnas

    @staticmethod
    def nula(m, n):
        """Matriz nula O_{m x n}: todas sus entradas son 0."""
        return Matriz([[0.0] * n for _ in range(m)])

    @staticmethod
    def identidad(n):
        """Matriz identidad I_n: <I_n>_ij = 1 si i = j, 0 si i != j."""
        return Matriz([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])

    def copia(self):
        return Matriz([fila[:] for fila in self.datos])

    # ------------------------------------------------------------------
    # Acceso con la notacion del curso
    # ------------------------------------------------------------------
    @property
    def tamano(self):
        return (self.m, self.n)

    def elemento(self, i, j):
        """<A>_ij, con 1 <= i <= m y 1 <= j <= n."""
        if not (1 <= i <= self.m):
            raise IndexError(f"Fila {i} fuera de rango: la matriz tiene {self.m} filas.")
        if not (1 <= j <= self.n):
            raise IndexError(f"Columna {j} fuera de rango: la matriz tiene {self.n} columnas.")
        return self.datos[i - 1][j - 1]

    def fila(self, i):
        """A_(i): i-esima fila, devuelta como matriz fila de 1 x n."""
        if not (1 <= i <= self.m):
            raise IndexError(f"Fila {i} fuera de rango: la matriz tiene {self.m} filas.")
        return Matriz([self.datos[i - 1][:]])

    def columna(self, j):
        """A^(j): j-esima columna, devuelta como matriz columna de m x 1."""
        if not (1 <= j <= self.n):
            raise IndexError(f"Columna {j} fuera de rango: la matriz tiene {self.n} columnas.")
        return Matriz([[self.datos[k][j - 1]] for k in range(self.m)])

    # ------------------------------------------------------------------
    # Clasificacion (Semana 3)
    # ------------------------------------------------------------------
    def es_cuadrada(self):
        return self.m == self.n

    def es_matriz_fila(self):
        return self.m == 1

    def es_matriz_columna(self):
        return self.n == 1

    def es_nula(self):
        return all(es_cero(x) for fila in self.datos for x in fila)

    def es_diagonal(self):
        if not self.es_cuadrada():
            return False
        return all(es_cero(self.datos[i][j])
                   for i in range(self.m) for j in range(self.n) if i != j)

    def es_identidad(self):
        if not self.es_cuadrada():
            return False
        for i in range(self.m):
            for j in range(self.n):
                esperado = 1.0 if i == j else 0.0
                if not es_cero(self.datos[i][j] - esperado):
                    return False
        return True

    def es_triangular_superior(self):
        """<A>_ij = 0 para todo i > j."""
        if not self.es_cuadrada():
            return False
        return all(es_cero(self.datos[i][j])
                   for i in range(self.m) for j in range(self.n) if i > j)

    def es_triangular_inferior(self):
        """<A>_ij = 0 para todo i < j."""
        if not self.es_cuadrada():
            return False
        return all(es_cero(self.datos[i][j])
                   for i in range(self.m) for j in range(self.n) if i < j)

    def clasificacion(self):
        """Lista de los tipos de matriz a los que pertenece A."""
        tipos = []
        if self.es_cuadrada():
            tipos.append(f"cuadrada de orden {self.m}")
        if self.es_matriz_fila():
            tipos.append("matriz fila")
        if self.es_matriz_columna():
            tipos.append("matriz columna (vector)")
        if self.es_nula():
            tipos.append("matriz nula")
        if self.es_identidad():
            tipos.append("matriz identidad")
        elif self.es_diagonal():
            tipos.append("matriz diagonal")
        if self.es_triangular_superior() and not self.es_diagonal():
            tipos.append("triangular superior")
        if self.es_triangular_inferior() and not self.es_diagonal():
            tipos.append("triangular inferior")
        if not tipos:
            tipos.append(f"matriz de tamano {self.m}x{self.n} sin tipo especial")
        return tipos

    # ------------------------------------------------------------------
    # Operaciones (Actividad #2)
    # ------------------------------------------------------------------
    def suma(self, otra):
        """<A+B>_ij = <A>_ij + <B>_ij. Exige matrices del mismo tamano."""
        if self.tamano != otra.tamano:
            raise ValueError(
                f"No se pueden sumar matrices de tamanos distintos: "
                f"{self.m}x{self.n} y {otra.m}x{otra.n}.")
        return Matriz([[self.datos[i][j] + otra.datos[i][j] for j in range(self.n)]
                       for i in range(self.m)])

    def por_escalar(self, lam):
        """<lambda*A>_ij = lambda * <A>_ij."""
        return Matriz([[lam * self.datos[i][j] for j in range(self.n)]
                       for i in range(self.m)])

    def resta(self, otra):
        """A - B = A + (-1 * B), tal como se define en clase."""
        return self.suma(otra.por_escalar(-1.0))

    def producto(self, otra):
        """
        A_{m x n} * B_{n x h} = C_{m x h}
        <C>_ij = suma_{k=1}^{n} <A>_ik * <B>_kj

        El producto NO es conmutativo: en general A*B != B*A.
        """
        if self.n != otra.m:
            raise ValueError(
                f"Producto no definido: A es {self.m}x{self.n} y B es {otra.m}x{otra.n}. "
                f"Las columnas de A deben coincidir con las filas de B.")
        resultado = []
        for i in range(self.m):
            fila = []
            for j in range(otra.n):
                acumulado = 0.0
                for k in range(self.n):
                    acumulado += self.datos[i][k] * otra.datos[k][j]
                fila.append(acumulado)
            resultado.append(fila)
        return Matriz(resultado)

    def detalle_producto(self, otra):
        """
        Desarrollo escrito de cada entrada del producto, tal como se hace a
        mano en clase:   <C>_11 = 2*2 + 4*0 + 0*1 = 4
        """
        if self.n != otra.m:
            raise ValueError("Producto no definido.")
        lineas = []
        for i in range(self.m):
            for j in range(otra.n):
                terminos = [f"{formatear(self.datos[i][k])}*{formatear(otra.datos[k][j])}"
                            for k in range(self.n)]
                valor = sum(self.datos[i][k] * otra.datos[k][j] for k in range(self.n))
                lineas.append(f"  <C>_{i + 1}{j + 1} = " + " + ".join(terminos)
                              + f" = {formatear(valor)}")
        return lineas

    def transpuesta(self):
        """A^t: <A^t>_ij = <A>_ji. Si A es m x n, entonces A^t es n x m."""
        return Matriz([[self.datos[i][j] for i in range(self.m)]
                       for j in range(self.n)])

    # ------------------------------------------------------------------
    # Comparacion e impresion
    # ------------------------------------------------------------------
    def igual_a(self, otra):
        """Igualdad: mismo tamano y <A>_ij = <B>_ij para todo i, j."""
        if self.tamano != otra.tamano:
            return False
        return all(es_cero(self.datos[i][j] - otra.datos[i][j])
                   for i in range(self.m) for j in range(self.n))

    def __str__(self):
        celdas = [[formatear(x) for x in fila] for fila in self.datos]
        anchos = [max(len(celdas[i][j]) for i in range(self.m)) for j in range(self.n)]
        return "\n".join(
            "| " + "  ".join(celdas[i][j].rjust(anchos[j]) for j in range(self.n)) + " |"
            for i in range(self.m))

    def __repr__(self):
        return f"Matriz({self.datos})"