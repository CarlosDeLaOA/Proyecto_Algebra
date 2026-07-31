"""
PixelForge MathEngine 2D v1.0
Modulo: historial.py

ACTIVIDAD #4: Historial de transformaciones.

Requisito de la consigna: "Toda transformacion aplicada debera quedar
registrada para permitir reconstruir el historial de modificaciones
realizadas sobre un objeto del escenario."

"""

from matrices import formatear


class Registro:
    """
    Una entrada del historial.

    matriz_usada puede ser None cuando la modificacion no proviene de una
    operacion matricial (por ejemplo, la optimizacion de vertices
    redundantes de la Actividad #3).
    """

    def __init__(self, numero, descripcion, operacion, matriz_usada, antes, despues):
        self.numero = numero
        self.descripcion = descripcion
        self.operacion = operacion      # "producto" | "suma" | "compuesta" | "estructural"
        self.matriz_usada = matriz_usada
        self.antes = list(antes)
        self.despues = list(despues)

    @staticmethod
    def _puntos(lista):
        return "; ".join(f"({formatear(x)}, {formatear(y)})" for x, y in lista)

    def simbolo(self):
        if self.operacion == "producto":
            return "A' = M * A"
        if self.operacion == "suma":
            return "A' = A + T"
        if self.operacion == "compuesta":
            return "A' = M * (A - C) + C"
        if self.operacion == "homogenea":
            return "A_h' = H * A_h   (coordenadas homogeneas)"
        return "modificacion estructural"

    def __str__(self):
        L = [f"[{self.numero}] {self.descripcion}",
             f"    Operacion: {self.simbolo()}"]
        if self.matriz_usada is not None:
            L.append("    Matriz utilizada:")
            L.extend("      " + linea for linea in str(self.matriz_usada).split("\n"))
        L.append(f"    Antes   ({len(self.antes)} vertices): {self._puntos(self.antes)}")
        L.append(f"    Despues ({len(self.despues)} vertices): {self._puntos(self.despues)}")
        return "\n".join(L)


class Historial:
    """Pila de registros asociada a un unico objeto del escenario."""

    def __init__(self, nombre_objeto, vertices_iniciales):
        self.nombre_objeto = nombre_objeto
        self.estado_inicial = list(vertices_iniciales)
        self.registros = []

    # ------------------------------------------------------------------
    # Registro
    # ------------------------------------------------------------------
    def registrar(self, resultado):
        """Agrega un objeto Resultado de transformaciones.py."""
        r = Registro(
            numero=len(self.registros) + 1,
            descripcion=resultado.descripcion,
            operacion=resultado.operacion,
            matriz_usada=resultado.matriz_usada,
            antes=resultado.figura_antes.vertices(),
            despues=resultado.figura_despues.vertices(),
        )
        self.registros.append(r)
        return r

    def registrar_evento(self, descripcion, antes, despues):
        """Agrega una modificacion que no proviene de una operacion matricial."""
        r = Registro(
            numero=len(self.registros) + 1,
            descripcion=descripcion,
            operacion="estructural",
            matriz_usada=None,
            antes=antes,
            despues=despues,
        )
        self.registros.append(r)
        return r

    # ------------------------------------------------------------------
    # Reconstruccion
    # ------------------------------------------------------------------
    def estado_actual(self):
        """Coordenadas despues de todas las transformaciones registradas."""
        if not self.registros:
            return list(self.estado_inicial)
        return list(self.registros[-1].despues)

    def reconstruir(self, paso):
        """
        Coordenadas del objeto tras los primeros 'paso' registros.
        paso = 0 devuelve el estado inicial.
        """
        if paso < 0 or paso > len(self.registros):
            raise IndexError(
                f"Paso {paso} fuera de rango: el historial tiene "
                f"{len(self.registros)} transformacion(es).")
        if paso == 0:
            return list(self.estado_inicial)
        return list(self.registros[paso - 1].despues)

    def deshacer(self):
        """Elimina el ultimo registro y devuelve las coordenadas previas."""
        if not self.registros:
            return list(self.estado_inicial)
        ultimo = self.registros.pop()
        return list(ultimo.antes)

    # ------------------------------------------------------------------
    # Presentacion
    # ------------------------------------------------------------------
    def cadena(self):
        """Resumen vertical:  Figura creada -> Rotacion -> Escalamiento ..."""
        pasos = [f"{self.nombre_objeto} creada  ({len(self.estado_inicial)} vertices)"]
        pasos += [f"{r.descripcion}" for r in self.registros]
        return "\n   |\n   v\n".join(pasos)

    def resumen(self):
        """Una linea por transformacion, con su numero."""
        if not self.registros:
            return "  (sin transformaciones registradas)"
        return "\n".join(f"  {r.numero}. {r.descripcion}" for r in self.registros)

    def detallado(self):
        if not self.registros:
            return "El historial no contiene transformaciones."
        return "\n\n".join(str(r) for r in self.registros)

    def __len__(self):
        return len(self.registros)


class GestorHistorial:
    """Mantiene un historial independiente por cada objeto del escenario."""

    def __init__(self):
        self.historiales = {}

    @staticmethod
    def _clave(nombre):
        return str(nombre).strip().lower()

    def iniciar(self, figura):
        """Crea el historial de un objeto recien construido."""
        self.historiales[self._clave(figura.nombre)] = Historial(
            figura.nombre, figura.vertices())

    def obtener(self, nombre):
        clave = self._clave(nombre)
        if clave not in self.historiales:
            raise KeyError(f"No hay historial para el objeto '{nombre}'.")
        return self.historiales[clave]

    def existe(self, nombre):
        return self._clave(nombre) in self.historiales

    def eliminar(self, nombre):
        self.historiales.pop(self._clave(nombre), None)

    def asegurar(self, nombre, vertices_iniciales):
        """Devuelve el historial del objeto; lo crea si todavia no existe."""
        clave = self._clave(nombre)
        if clave not in self.historiales:
            self.historiales[clave] = Historial(nombre, vertices_iniciales)
        return self.historiales[clave]

    def registrar_secuencia(self, nombre_destino, figura_origen, resultados):
        """
        Registra una o varias transformaciones sobre el objeto destino.

        Si el destino es un objeto nuevo, su historial arranca en el estado
        del objeto de origen, de modo que la cadena completa queda visible.
        """
        h = self.asegurar(nombre_destino, figura_origen.vertices())
        for r in resultados:
            h.registrar(r)
        return h

    def registrar_evento(self, nombre_destino, figura_origen, descripcion,
                         antes, despues):
        h = self.asegurar(nombre_destino, figura_origen.vertices())
        return h.registrar_evento(descripcion, antes, despues)

    def objetos_con_historial(self):
        return [h.nombre_objeto for h in self.historiales.values()]