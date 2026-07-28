"""
PixelForge MathEngine 2D v1.0
Modulo: main.py

Interfaz de consola del motor grafico.
Actividades habilitadas: #1 (representacion), #2 (transformaciones) y
#3 (analisis matematico del escenario).

Principios de la interfaz:
  - El escenario arranca VACIO. Ninguna figura viene predeterminada.
  - Los graficos se generan solo cuando el usuario los pide.
  - Ningun resultado se guarda sin que el usuario decida que hacer con el.
"""

import transformaciones as tr
import analisis
import graficos
from figuras import Figura, Escenario

SEP = "-" * 58


# ----------------------------------------------------------------------
# Utilidades de entrada
# ----------------------------------------------------------------------
def leer_numero(mensaje):
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            print("  Entrada invalida: escriba un numero.")


def leer_entero_positivo(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor < minimo:
                print(f"  Debe ser un entero mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Entrada invalida: escriba un numero entero.")


def leer_opcion(mensaje, validas):
    while True:
        op = input(mensaje).strip().lower()
        if op in validas:
            return op
        print(f"  Opcion invalida. Use: {', '.join(sorted(validas))}")


def elegir_objeto(escenario, accion="operar"):
    """Devuelve un objeto del escenario, o None si no hay o se cancela."""
    if len(escenario) == 0:
        print("\n  El escenario esta vacio. Cree un objeto primero.")
        return None
    print("\nObjetos disponibles:")
    print(escenario.listar())
    nombre = input(f"  Nombre del objeto a {accion} (vacio = cancelar): ").strip()
    if not nombre:
        return None
    try:
        return escenario.obtener(nombre)
    except KeyError as e:
        print(f"  {e}")
        return None


def guardar_resultado(escenario, figura_original, vertices_nuevos, etiqueta):
    """Pregunta que hacer con una figura resultante y la guarda si corresponde."""
    print(f"\n  Que desea hacer con {etiqueta}?")
    print("    1) Reemplazar el objeto en el escenario")
    print("    2) Guardarlo como un objeto nuevo")
    print("    3) Descartarlo")
    destino = leer_opcion("  Opcion: ", {"1", "2", "3"})

    if destino == "1":
        escenario.reemplazar(figura_original.nombre,
                             Figura(figura_original.nombre, vertices_nuevos))
        print(f"  Objeto '{figura_original.nombre}' actualizado.")
    elif destino == "2":
        nuevo = input("    Nombre del objeto nuevo: ").strip()
        try:
            escenario.agregar(Figura(nuevo, vertices_nuevos))
            print(f"  Objeto '{nuevo}' agregado al escenario.")
        except (ValueError, TypeError) as e:
            print(f"  No se pudo guardar: {e}")
    else:
        print("  Resultado descartado. El escenario no cambio.")


# ----------------------------------------------------------------------
# ACTIVIDAD #1: representacion de objetos
# ----------------------------------------------------------------------
def crear_objeto(escenario):
    print("\nConstruccion de un objeto por coordenadas cartesianas")
    nombre = input("  Nombre del objeto: ").strip()
    if not nombre:
        print("  Operacion cancelada: el nombre no puede estar vacio.")
        return

    cantidad = leer_entero_positivo("  Cantidad de vertices: ", minimo=1)
    if cantidad < 3:
        print("  Aviso: con menos de 3 vertices el objeto no es un poligono.")

    puntos = []
    for k in range(cantidad):
        print(f"  Vertice P{k + 1}:")
        puntos.append((leer_numero("    x: "), leer_numero("    y: ")))

    try:
        figura = escenario.agregar(Figura(nombre, puntos))
    except (ValueError, TypeError) as e:
        print(f"  No se pudo crear el objeto: {e}")
        return

    print(f"\n  Objeto '{figura.nombre}' agregado al escenario.")
    print(SEP)
    print(figura.detalle())
    print(SEP)


def ver_objeto(escenario):
    figura = elegir_objeto(escenario, "consultar")
    if figura is None:
        return
    print(SEP)
    print(figura.detalle())
    print(SEP)

    if leer_opcion("  Ver un vertice como matriz columna? (s/n): ",
                   {"s", "n"}) == "s":
        j = leer_entero_positivo(
            f"    Numero de vertice (1 a {figura.cantidad_vertices}): ")
        try:
            print(f"    P{j} = A^({j}) =")
            print(figura.vector_posicion(j))
        except IndexError as e:
            print(f"    {e}")


def eliminar_objeto(escenario):
    figura = elegir_objeto(escenario, "eliminar")
    if figura is None:
        return
    escenario.eliminar(figura.nombre)
    print(f"  Objeto '{figura.nombre}' eliminado.")


# ----------------------------------------------------------------------
# ACTIVIDAD #2: transformaciones geometricas
# ----------------------------------------------------------------------
def pedir_centro():
    """Pregunta si la transformacion es respecto al origen o a otro punto."""
    print("  Punto de referencia:")
    print("    1) El origen (0, 0)")
    print("    2) Otro punto")
    if leer_opcion("  Opcion: ", {"1", "2"}) == "1":
        return None
    return (leer_numero("    cx: "), leer_numero("    cy: "))


def pedir_transformacion_simple(figura):
    print("\n  Transformacion")
    print("    1) Trasladar   (suma:     A' = A + T)")
    print("    2) Rotar       (producto: A' = R * A)")
    print("    3) Escalar     (producto: A' = S * A)")
    print("    4) Reflejar    (producto: A' = F * A)")
    op = leer_opcion("  Opcion: ", {"1", "2", "3", "4"})

    if op == "1":
        return tr.trasladar(figura, leer_numero("    tx: "),
                            leer_numero("    ty: "))

    if op == "2":
        ang = leer_numero("    Angulo en grados: ")
        return tr.rotar(figura, ang, centro=pedir_centro())

    if op == "3":
        sx = leer_numero("    Factor sx: ")
        if leer_opcion("    Escalamiento uniforme? (s/n): ", {"s", "n"}) == "s":
            sy = None
        else:
            sy = leer_numero("    Factor sy: ")
        return tr.escalar(figura, sx, sy, centro=pedir_centro())

    eje = leer_opcion(f"    Eje ({' / '.join(tr.EJES_REFLEXION)}): ",
                      set(tr.EJES_REFLEXION.keys()))
    return tr.reflejar(figura, eje)


def pedir_secuencia(figura):
    print("\n  Ingrese las transformaciones EN ORDEN. Escriba 'fin' para terminar.")
    print("  Comandos: trasladar / rotar / escalar / reflejar / fin")
    operaciones = []
    while True:
        cmd = input(f"  [{len(operaciones)} cargadas] > ").strip().lower()
        if cmd == "fin":
            break
        if cmd == "rotar":
            operaciones.append(("rotar", leer_numero("      Angulo: ")))
        elif cmd == "escalar":
            operaciones.append(("escalar", leer_numero("      Factor: ")))
        elif cmd == "trasladar":
            operaciones.append(("trasladar", (leer_numero("      tx: "),
                                              leer_numero("      ty: "))))
        elif cmd == "reflejar":
            operaciones.append(
                ("reflejar",
                 leer_opcion(f"      Eje ({' / '.join(tr.EJES_REFLEXION)}): ",
                             set(tr.EJES_REFLEXION.keys()))))
        else:
            print("      Comando no reconocido.")

    if not operaciones:
        return []
    _, resultados = tr.aplicar_secuencia(figura, operaciones)
    return resultados


def aplicar_transformacion(escenario, estado):
    figura = elegir_objeto(escenario, "transformar")
    if figura is None:
        return

    print("\n  Modo")
    print("    1) Una sola transformacion")
    print("    2) Varias transformaciones consecutivas")
    modo = leer_opcion("  Opcion: ", {"1", "2"})

    try:
        resultados = [pedir_transformacion_simple(figura)] if modo == "1" \
            else pedir_secuencia(figura)
    except (ValueError, KeyError) as e:
        print(f"  No se pudo aplicar la transformacion: {e}")
        return

    if not resultados:
        print("  No se aplico ninguna transformacion.")
        return

    for k, r in enumerate(resultados, start=1):
        print("\n" + SEP)
        if len(resultados) > 1:
            print(f"PASO {k} de {len(resultados)}")
            print(SEP)
        print(r.informe())
        print(SEP)

    # Si todas las transformaciones fueron LINEALES, mostrar la matriz
    # equivalente. Las traslaciones no pueden incluirse por no ser lineales.
    lineales = [r.matriz_usada for r in resultados if r.operacion == "producto"]
    if len(lineales) > 1 and len(lineales) == len(resultados):
        print("\nMatriz compuesta equivalente  M = Mk * ... * M1:")
        print(tr.matriz_compuesta(lineales))
        print("Aplicar esta unica matriz produce el mismo resultado que aplicar")
        print("las transformaciones una por una (asociatividad del producto).")
        print(SEP)

    estado["ultimo"] = resultados[-1]
    guardar_resultado(escenario, figura,
                      resultados[-1].figura_despues.vertices(),
                      "la figura transformada")


# ----------------------------------------------------------------------
# ACTIVIDAD #3: analisis matematico del escenario
# ----------------------------------------------------------------------
def analisis_subespacio(escenario):
    print("\n  Restriccion de movimiento de la forma  a*x + b*y = c")
    print("  (por ejemplo, a=1  b=1  c=10  describe la recta x + y = 10)")
    a = leer_numero("    a: ")
    b = leer_numero("    b: ")
    c = leer_numero("    c: ")

    muestra = None
    if len(escenario) > 0:
        if leer_opcion("  Verificar los vertices de un objeto? (s/n): ",
                       {"s", "n"}) == "s":
            figura = elegir_objeto(escenario, "verificar")
            if figura is not None:
                muestra = figura.vertices()

    try:
        _, lineas = analisis.verificar_subespacio_recta(a, b, c, muestra)
    except ValueError as e:
        print(f"  {e}")
        return
    print(SEP)
    print("\n".join(lineas))
    print(SEP)


def analisis_independencia(escenario):
    figura = elegir_objeto(escenario, "analizar")
    if figura is None:
        return
    etiquetas = [f"P{k + 1}" for k in range(figura.cantidad_vertices)]
    print(SEP)
    print(f"Vectores de posicion de los vertices de '{figura.nombre}'")
    print(SEP)
    print(analisis.informe_conjunto(figura.vertices(), etiquetas))
    print(SEP)
    print("Nota: los vectores de posicion viven en R^2, de modo que la")
    print("dimension nunca puede superar 2. Para optimizar la figura use la")
    print("opcion de vertices redundantes, que analiza las aristas.")
    print(SEP)


def analisis_redundancia(escenario):
    figura = elegir_objeto(escenario, "optimizar")
    if figura is None:
        return
    lineas, optimizada = analisis.informe_redundancia(figura)
    print(SEP)
    print("\n".join(lineas))
    print(SEP)

    if len(optimizada) == figura.cantidad_vertices:
        return
    guardar_resultado(escenario, figura, optimizada,
                      "la representacion optimizada")


def analisis_escenario(escenario):
    """Analiza en conjunto todos los vertices almacenados en el escenario."""
    if len(escenario) == 0:
        print("\n  El escenario esta vacio.")
        return
    vectores = []
    etiquetas = []
    for objeto in escenario.objetos:
        for k, p in enumerate(objeto.vertices()):
            vectores.append(p)
            etiquetas.append(f"{objeto.nombre[:6]}.P{k + 1}")
    print(SEP)
    print(f"Analisis conjunto de {len(vectores)} vertices "
          f"de {len(escenario)} objeto(s)")
    print(SEP)
    print(analisis.informe_conjunto(vectores, etiquetas))
    print(SEP)


def menu_analisis(escenario):
    print("\n  Analisis matematico del escenario")
    print("    1) Espacios y subespacios vectoriales")
    print("    2) Independencia lineal, base y dimension de un objeto")
    print("    3) Detectar vertices redundantes (optimizar un objeto)")
    print("    4) Analizar todos los objetos del escenario en conjunto")
    op = leer_opcion("  Opcion: ", {"1", "2", "3", "4"})

    if op == "1":
        analisis_subespacio(escenario)
    elif op == "2":
        analisis_independencia(escenario)
    elif op == "3":
        analisis_redundancia(escenario)
    else:
        analisis_escenario(escenario)


# ----------------------------------------------------------------------
# Representacion grafica
# ----------------------------------------------------------------------
def ver_grafico(escenario, estado):
    print("\n  Que desea graficar?")
    print("    1) Un objeto del escenario")
    print("    2) La ultima transformacion aplicada (original vs transformada)")
    op = leer_opcion("  Opcion: ", {"1", "2"})

    if op == "1":
        figura = elegir_objeto(escenario, "graficar")
        if figura is None:
            return
        original, transformada, titulo = figura, None, figura.nombre
        archivo = f"{figura.nombre.lower().replace(' ', '_')}.png"
    else:
        r = estado.get("ultimo")
        if r is None:
            print("  Todavia no se ha aplicado ninguna transformacion.")
            return
        original = r.figura_antes
        transformada = r.figura_despues
        titulo = r.descripcion
        archivo = "ultima_transformacion.png"

    ruta = graficos.graficar(original, transformada, titulo=titulo,
                             nombre_archivo=archivo)
    if ruta:
        print(f"  Grafico guardado en: {ruta}")
    else:
        print("  matplotlib no esta instalado. Grafico en modo texto:")
        print(graficos.grafico_texto(transformada or original))


# ----------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------
def main():
    print("=" * 58)
    print("     PixelForge MathEngine 2D v1.0")
    print("     Actividades habilitadas: #1, #2 y #3")
    print("=" * 58)

    escenario = Escenario()
    estado = {"ultimo": None}

    while True:
        print("\n" + SEP)
        print(f"Escenario: {len(escenario)} objeto(s)")
        print(escenario.listar())
        print(SEP)
        print("  1) Crear objeto por coordenadas")
        print("  2) Ver detalle de un objeto")
        print("  3) Aplicar transformacion")
        print("  4) Analisis matematico del escenario")
        print("  5) Ver grafico")
        print("  6) Eliminar un objeto")
        print("  0) Salir")

        op = leer_opcion("Opcion: ", {"0", "1", "2", "3", "4", "5", "6"})
        if op == "0":
            print("Cerrando MathEngine 2D.")
            break
        elif op == "1":
            crear_objeto(escenario)
        elif op == "2":
            ver_objeto(escenario)
        elif op == "3":
            aplicar_transformacion(escenario, estado)
        elif op == "4":
            menu_analisis(escenario)
        elif op == "5":
            ver_grafico(escenario, estado)
        elif op == "6":
            eliminar_objeto(escenario)


if __name__ == "__main__":
    main()