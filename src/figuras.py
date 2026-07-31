from matrices import Matriz, formatear, es_cero
class Figura:
    """Objeto bidimensional del escenario, representado por una matriz 2 x n."""

    def __init__(self, nombre, vertices):
        """
        nombre   : identificador del objeto (Jugador, Enemigo, Plataforma, ...)
        vertices : lista de pares (x, y) con las coordenadas cartesianas
        """
        nombre = str(nombre).strip()
        if not nombre:
            raise ValueError("El objeto debe tener un nombre.")

        vertices = self._validar_vertices(vertices)

        self.nombre = nombre
        self.matriz = Matriz([
            [float(p[0]) for p in vertices],
            [float(p[1]) for p in vertices],
        ])

    # ------------------------------------------------------------------
    # Validacion de la entrada
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_vertices(vertices):
        if not isinstance(vertices, (list, tuple)) or len(vertices) == 0:
            raise ValueError("Debe indicar al menos un vertice.")

        limpios = []
        for k, p in enumerate(vertices):
            if not isinstance(p, (list, tuple)) or len(p) != 2:
                raise ValueError(
                    f"El vertice {k + 1} debe ser un par (x, y); se recibio {p!r}.")
            x, y = p
            for valor in (x, y):
                if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                    raise TypeError(
                        f"La coordenada {valor!r} del vertice {k + 1} no es un numero real.")
            limpios.append((float(x), float(y)))

        # Dos vertices consecutivos identicos generarian una arista nula,
        # que rompe el analisis geometrico de la Actividad #3.
        for k in range(len(limpios) - 1):
            if es_cero(limpios[k][0] - limpios[k + 1][0]) and \
               es_cero(limpios[k][1] - limpios[k + 1][1]):
                raise ValueError(
                    f"Los vertices {k + 1} y {k + 2} son iguales: "
                    "no se admiten vertices consecutivos repetidos.")

        return limpios

    # ------------------------------------------------------------------
    # Construccion alterna
    # ------------------------------------------------------------------
    @classmethod
    def desde_matriz(cls, nombre, matriz):
        """
        Reconstruye una figura a partir de su matriz.

        Admite DOS representaciones:

          - CARTESIANA, matriz de 2 x n:
                | x1  x2  ...  xn |
                | y1  y2  ...  yn |

          - HOMOGENEA, matriz de 3 x n:
                | x1  x2  ...  xn |
                | y1  y2  ...  yn |
                | w1  w2  ...  wn |

        En la forma homogenea, el punto cartesiano de la columna j se obtiene
        dividiendo entre wj:   (xj/wj , yj/wj).

        Habitualmente wj = 1, porque las transformaciones afines conservan esa
        componente. La division general se implementa igual, para que la
        conversion sea correcta si en el futuro se incorporan transformaciones
        proyectivas, donde w si cambia.

        Un valor wj = 0 representa un punto en el infinito (una direccion, no
        una posicion) y no tiene equivalente cartesiano, por lo que se rechaza.
        """
        if matriz.m == 2:
            puntos = [(matriz.datos[0][j], matriz.datos[1][j])
                      for j in range(matriz.n)]
            return cls(nombre, puntos)

        if matriz.m == 3:
            puntos = []
            for j in range(matriz.n):
                w = matriz.datos[2][j]
                if es_cero(w):
                    raise ValueError(
                        f"La columna {j+1} tiene w = 0: representa un punto en el "
                        "infinito y no admite conversion a coordenadas cartesianas.")
                puntos.append((matriz.datos[0][j] / w, matriz.datos[1][j] / w))
            return cls(nombre, puntos)

        raise ValueError(
            f"La matriz de una figura 2D debe tener 2 filas (cartesiana) o "
            f"3 filas; la recibida tiene {matriz.m}.")

    # ------------------------------------------------------------------
    # Consulta
    # ------------------------------------------------------------------
    @property
    def cantidad_vertices(self):
        return self.matriz.n

    def vertices(self):
        """Lista de pares (x, y), leyendo la matriz columna por columna."""
        return [(self.matriz.datos[0][j], self.matriz.datos[1][j])
                for j in range(self.matriz.n)]

    def vertice(self, j):
        """P_j = A^(j): el vertice j-esimo como par (x, y). Indice 1-based."""
        return (self.matriz.elemento(1, j), self.matriz.elemento(2, j))

    def vector_posicion(self, j):
        """P_j como matriz columna de M_{2 x 1}(R), tal como se define en clase."""
        return self.matriz.columna(j)
    def vector_posicion_homogeneo(self, j):
        """
        P_j como matriz columna de M_{3 x 1}(R), en coordenadas homogeneas.

        Es la j-esima columna de la matriz homogenea: las mismas coordenadas
        cartesianas mas la componente w = 1.
        """
        return self.matriz_homogenea().columna(j)
    def es_poligono(self):
        """Un poligono requiere al menos 3 vertices."""
        return self.cantidad_vertices >= 3
    def matriz_homogenea(self):
        """
        Devuelve la figura en COORDENADAS HOMOGENEAS: una matriz de 3 x n
        formada agregando una tercera fila constante igual a 1.

                | x1  x2  ...  xn |
                | y1  y2  ...  yn |
                |  1   1  ...   1 |

        Esta representacion permite expresar la traslacion como un PRODUCTO de
        matrices de 3x3, en lugar de como una suma, y por lo tanto condensar
        cualquier secuencia de transformaciones (incluidas las traslaciones)
        en una unica matriz.

        La figura sigue almacenandose internamente en forma cartesiana de
        2 x n: esta es una vista alterna que se construye cuando se pide.
        """
        return Matriz([
            self.matriz.datos[0][:],
            self.matriz.datos[1][:],
            [1.0] * self.matriz.n,
        ])

    # ------------------------------------------------------------------
    # Presentacion
    # ------------------------------------------------------------------
    def texto_vertices(self):
        return "\n".join(
            f"  P{j + 1} = ({formatear(x)}, {formatear(y)})"
            for j, (x, y) in enumerate(self.vertices()))

    def detalle(self, incluir_homogenea=False):
        """
        Ficha completa del objeto para mostrar en la interfaz.

        Si incluir_homogenea es True, agrega al final la representacion en
        coordenadas homogeneas (matriz de 3 x n).
        """
        L = []
        L.append(f"Objeto: {self.nombre}")
        L.append(f"Cantidad de vertices: {self.cantidad_vertices}")
        L.append(f"Tipo: {'poligono' if self.es_poligono() else 'punto o segmento'}")
        L.append("")
        L.append(f"Matriz asociada A en M_{{{self.matriz.m} x {self.matriz.n}}}(R):")
        L.append(str(self.matriz))
        L.append("Clasificacion de A: " + ", ".join(self.matriz.clasificacion()))
        L.append("")
        L.append("Coordenadas cartesianas (cada columna A^(j) es un vertice):")
        L.append(self.texto_vertices())
        L.append("")
        L.append("Filas de A:")
        L.append(f"  A_(1) = {self.matriz.fila(1)}   ")
        L.append(f"  A_(2) = {self.matriz.fila(2)}   ")
        if incluir_homogenea:
            H = self.matriz_homogenea()
            L.append("")
            L.append(f"Representacion homogenea, A_h en M_{{3 x {H.n}}}(R):")
            L.append(str(H))
        return "\n".join(L)

    def __str__(self):
        return (f"{self.nombre} ({self.cantidad_vertices} vertices)\n"
                f"{self.matriz}")

    def __repr__(self):
        return f"Figura({self.nombre!r}, {self.vertices()})"


class Escenario:
    """
    Coleccion de objetos del mundo virtual.

    La Actividad #3 pide "analizar los objetos almacenados", de modo que el
    motor necesita un contenedor y no solo figuras sueltas.
    """

    def __init__(self):
        self.objetos = []

    def agregar(self, figura):
        if not isinstance(figura, Figura):
            raise TypeError("Solo se pueden agregar objetos de tipo Figura.")
        if any(o.nombre.lower() == figura.nombre.lower() for o in self.objetos):
            raise ValueError(f"Ya existe un objeto llamado '{figura.nombre}'.")
        self.objetos.append(figura)
        return figura

    def obtener(self, nombre):
        for o in self.objetos:
            if o.nombre.lower() == str(nombre).strip().lower():
                return o
        raise KeyError(f"No existe un objeto llamado '{nombre}'.")

    def eliminar(self, nombre):
        objeto = self.obtener(nombre)
        self.objetos.remove(objeto)
        return objeto

    def reemplazar(self, nombre, figura_nueva):
        """Sustituye un objeto conservando su posicion en la lista."""
        objeto = self.obtener(nombre)
        self.objetos[self.objetos.index(objeto)] = figura_nueva
        return figura_nueva

    def nombres(self):
        return [o.nombre for o in self.objetos]

    def listar(self):
        if not self.objetos:
            return "El escenario esta vacio."
        return "\n".join(
            f"  {k + 1}. {o.nombre}  ->  matriz de {o.matriz.m}x{o.matriz.n} "
            f"({o.cantidad_vertices} vertices)"
            for k, o in enumerate(self.objetos))

    def __len__(self):
        return len(self.objetos)