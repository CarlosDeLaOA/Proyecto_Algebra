"""
PixelForge MathEngine 2D v1.0
Modulo: main.py

Interfaz de consola del motor grafico.
Actividades habilitadas: #1 (representacion), #2 (transformaciones),
#3 (analisis matematico) y #4 (historial de transformaciones).

"""

import transformaciones as tr
import analisis
import graficos
from figuras import Figura, Escenario
from historial import GestorHistorial
from matrices import formatear, Matriz

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


def leer_fila(mensaje, cantidad):
    """
    Lee una fila completa de una matriz: varios numeros en una sola linea,
    separados por espacios o comas.
    """
    while True:
        texto = input(mensaje).strip().replace(",", " ")
        partes = texto.split()
        if len(partes) != cantidad:
            print(f"  Debe ingresar exactamente {cantidad} numeros separados por espacios.")
            continue
        try:
            return [float(p) for p in partes]
        except ValueError:
            print("  Todos los valores deben ser numeros.")


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
    """
    Pregunta que hacer con una figura resultante.
    Devuelve el nombre del objeto donde quedo guardada, o None si se descarto.
    """
    print(f"\n  Que desea hacer con {etiqueta}?")
    print("    1) Reemplazar el objeto en el escenario")
    print("    2) Guardarlo como un objeto nuevo")
    print("    3) Descartarlo")
    destino = leer_opcion("  Opcion: ", {"1", "2", "3"})

    if destino == "1":
        escenario.reemplazar(figura_original.nombre,
                             Figura(figura_original.nombre, vertices_nuevos))
        print(f"  Objeto '{figura_original.nombre}' actualizado.")
        return figura_original.nombre

    if destino == "2":
        nuevo = input("    Nombre del objeto nuevo: ").strip()
        try:
            escenario.agregar(Figura(nuevo, vertices_nuevos))
            print(f"  Objeto '{nuevo}' agregado al escenario.")
            return nuevo
        except (ValueError, TypeError) as e:
            print(f"  No se pudo guardar: {e}")
            return None

    print("  Resultado descartado. El escenario no cambio.")
    return None


# ----------------------------------------------------------------------
# ACTIVIDAD #1: representacion de objetos
# ----------------------------------------------------------------------
def crear_objeto(escenario, gestor):
    """Menu de construccion: por coordenadas o por matriz."""
    print("\n  Como desea construir el objeto?")
    print("    1) Ingresando sus coordenadas cartesianas, vertice por vertice")
    print("    2) Ingresando directamente su matriz")
    if leer_opcion("  Opcion: ", {"1", "2"}) == "1":
        crear_por_coordenadas(escenario, gestor)
    else:
        crear_por_matriz(escenario, gestor)


def crear_por_coordenadas(escenario, gestor):
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

    gestor.iniciar(figura)
    print(f"\n  Objeto '{figura.nombre}' agregado al escenario.")
    print(SEP)
    print(figura.detalle())
    print(SEP)


def crear_por_matriz(escenario, gestor):
    """
    Construye un objeto ingresando su matriz fila por fila.

    Admite las dos representaciones que acepta Figura.desde_matriz:
    de 2 filas (coordenadas cartesianas) o de 3 filas (coordenadas
    homogeneas). La interfaz no menciona esos nombres tecnicos: describe
    directamente que contiene cada fila.
    """
    print("\nConstruccion de un objeto ingresando su matriz")
    print("  Representaciones admitidas:")
    print("    2 filas:  fila 1 = abscisas, fila 2 = ordenadas")
    print("    3 filas:  se agrega la fila de componentes w")

    nombre = input("  Nombre del objeto: ").strip()
    if not nombre:
        print("  Operacion cancelada: el nombre no puede estar vacio.")
        return

    filas = int(leer_opcion("  Cantidad de filas: ", {"2", "3"}))
    columnas = leer_entero_positivo("  Cantidad de columnas (vertices): ", minimo=1)

    print(f"  Ingrese cada fila con {columnas} numero(s) separados por espacios.")
    etiquetas = ["abscisas (x)", "ordenadas (y)", "componentes (w)"]
    datos = []
    for i in range(filas):
        datos.append(leer_fila(f"    Fila {i + 1} - {etiquetas[i]}: ", columnas))

    try:
        M = Matriz(datos)
        figura = escenario.agregar(Figura.desde_matriz(nombre, M))
    except (ValueError, TypeError) as e:
        print(f"  No se pudo crear el objeto: {e}")
        return

    gestor.iniciar(figura)
    print(f"\n  Matriz ingresada ({M.m}x{M.n}):")
    print(M)
    if filas == 3:
        print("  Convertida dividiendo cada columna entre su componente w.")
    print(f"\n  Objeto '{figura.nombre}' agregado al escenario.")
    print(SEP)
    print(figura.detalle())
    print(SEP)


def ver_objeto(escenario):
    figura = elegir_objeto(escenario, "consultar")
    if figura is None:
        return

    homogenea = leer_opcion("  Mostrar tambien la representacion homogenea? (s/n): ",
                            {"s", "n"}) == "s"
    print(SEP)
    print(figura.detalle(incluir_homogenea=homogenea))
    print(SEP)

    if leer_opcion("  Ver un vertice como matriz columna? (s/n): ",
                   {"s", "n"}) == "s":
        j = leer_entero_positivo(
            f"    Numero de vertice (1 a {figura.cantidad_vertices}): ")
        try:
            print(f"    P{j} = A^({j}) =")
            print(figura.vector_posicion(j))
            if homogenea:
                print(f"    En coordenadas homogeneas, A_h^({j}) =")
                print(figura.vector_posicion_homogeneo(j))
        except IndexError as e:
            print(f"    {e}")


def eliminar_objeto(escenario, gestor):
    figura = elegir_objeto(escenario, "eliminar")
    if figura is None:
        return
    escenario.eliminar(figura.nombre)
    gestor.eliminar(figura.nombre)
    print(f"  Objeto '{figura.nombre}' eliminado, junto con su historial.")


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
    print("    1) Trasladar   ")
    print("    2) Rotar       ")
    print("    3) Escalar     ")
    print("    4) Reflejar    ")
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


def pedir_operaciones():
    """
    Lee una lista de operaciones sin aplicarlas todavia.

    Se usa tanto en el modo cartesiano como en el homogeneo, porque el
    formato de la lista es el mismo en ambos casos.
    """
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
    return operaciones


def pedir_secuencia(figura):
    """Modo cartesiano: aplica las transformaciones una por una."""
    operaciones = pedir_operaciones()
    if not operaciones:
        return []
    _, resultados = tr.aplicar_secuencia(figura, operaciones)
    return resultados


def transformar_homogenea(escenario, gestor, figura, estado):
    """
    Modo homogeneo: aplica una secuencia de transformaciones condensandolas
    en una unica matriz de 3x3.

    A diferencia del modo cartesiano, aqui la traslacion tambien es un
    producto, de modo que la matriz compuesta puede incluirla.
    """
    print("\n  Modo homogeneo: las cuatro transformaciones son productos de")
    print("  matrices de 3x3 y toda la secuencia se condensa en una sola matriz.")

    operaciones = pedir_operaciones()
    if not operaciones:
        print("  No se aplico ninguna transformacion.")
        return

    try:
        final, H_total, resultado, pasos = tr.aplicar_secuencia_homogenea(
            figura, operaciones)
    except (ValueError, KeyError) as e:
        print(f"  No se pudo aplicar la transformacion: {e}")
        return

    print("\n" + SEP)
    print("Matrices homogeneas individuales")
    print(SEP)
    for k, (desc, H) in enumerate(pasos, start=1):
        print(f"\nM{k} - {desc}:")
        print(H)

    print("\n" + SEP)
    print(f"Matriz compuesta  H = M{len(pasos)} * ... * M1")
    print(SEP)
    print(H_total)
    print("\nLa tercera columna contiene la traslacion acumulada, y la tercera")
    print("fila (0, 0, 1) preserva la componente w.")

    print("\n" + SEP)
    print(resultado.informe())
    print(SEP)

    estado["ultimo"] = resultado
    destino = guardar_resultado(escenario, figura,
                                resultado.figura_despues.vertices(),
                                "la figura transformada")
    if destino:
        gestor.registrar_secuencia(destino, figura, [resultado])
        print(f"  Transformacion registrada en el historial de '{destino}'.")


def aplicar_transformacion(escenario, gestor, estado):
    figura = elegir_objeto(escenario, "transformar")
    if figura is None:
        return

    print("\n  Modo")
    print("    1) Una sola transformacion")
    print("    2) Varias transformaciones consecutivas (cartesiano, 2x2)")
    print("    3) Varias transformaciones con matriz compuesta 3x3 (homogeneas)")
    modo = leer_opcion("  Opcion: ", {"1", "2", "3"})

    if modo == "3":
        transformar_homogenea(escenario, gestor, figura, estado)
        return

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
    # equivalente. Las traslaciones no pueden incluirse en modo cartesiano
    # por no ser lineales; para eso esta el modo homogeneo.
    lineales = [r.matriz_usada for r in resultados if r.operacion == "producto"]
    if len(lineales) > 1 and len(lineales) == len(resultados):
        print("\nMatriz compuesta equivalente  M = Mk * ... * M1:")
        print(tr.matriz_compuesta(lineales))
        print("Aplicar esta unica matriz produce el mismo resultado que aplicar")
        print("las transformaciones una por una (asociatividad del producto).")
        print(SEP)

    estado["ultimo"] = resultados[-1]
    destino = guardar_resultado(escenario, figura,
                                resultados[-1].figura_despues.vertices(),
                                "la figura transformada")
    if destino:
        gestor.registrar_secuencia(destino, figura, resultados)
        print(f"  {len(resultados)} transformacion(es) registrada(s) en el "
              f"historial de '{destino}'.")


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


def analisis_redundancia(escenario, gestor):
    figura = elegir_objeto(escenario, "optimizar")
    if figura is None:
        return
    lineas, optimizada = analisis.informe_redundancia(figura)
    print(SEP)
    print("\n".join(lineas))
    print(SEP)

    if len(optimizada) == figura.cantidad_vertices:
        return

    destino = guardar_resultado(escenario, figura, optimizada,
                                "la representacion optimizada")
    if destino:
        gestor.registrar_evento(
            destino, figura,
            f"Optimizacion: {figura.cantidad_vertices} -> {len(optimizada)} vertices",
            figura.vertices(), optimizada)
        print(f"  Optimizacion registrada en el historial de '{destino}'.")


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


def menu_analisis(escenario, gestor):
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
        analisis_redundancia(escenario, gestor)
    else:
        analisis_escenario(escenario)


# ----------------------------------------------------------------------
# ACTIVIDAD #4: historial de transformaciones
# ----------------------------------------------------------------------
def menu_historial(escenario, gestor):
    figura = elegir_objeto(escenario, "consultar el historial de")
    if figura is None:
        return
    try:
        h = gestor.obtener(figura.nombre)
    except KeyError as e:
        print(f"  {e}")
        return

    print(SEP)
    print(f"Historial de '{h.nombre_objeto}': "
          f"{len(h)} transformacion(es) registrada(s)")
    print(SEP)
    print(h.cadena())
    print(SEP)

    if len(h) == 0:
        return

    print("\n  1) Ver el detalle completo (matrices y coordenadas)")
    print("  2) Reconstruir el objeto en un paso anterior")
    print("  3) Deshacer la ultima transformacion")
    print("  4) Volver")
    op = leer_opcion("  Opcion: ", {"1", "2", "3", "4"})

    if op == "1":
        print(SEP)
        print(h.detallado())
        print(SEP)

    elif op == "2":
        print("\n  Pasos disponibles:")
        print(f"  0. Estado inicial ({len(h.estado_inicial)} vertices)")
        print(h.resumen())
        paso = leer_entero_positivo("  Reconstruir hasta el paso: ", minimo=0)
        try:
            puntos = h.reconstruir(paso)
        except IndexError as e:
            print(f"  {e}")
            return
        print(f"\n  Coordenadas tras {paso} transformacion(es):")
        for k, (x, y) in enumerate(puntos):
            print(f"    P{k + 1} = ({formatear(x)}, {formatear(y)})")
        if leer_opcion("  Restaurar el objeto a este estado? (s/n): ",
                       {"s", "n"}) == "s":
            escenario.reemplazar(figura.nombre, Figura(figura.nombre, puntos))
            h.registros = h.registros[:paso]
            print(f"  Objeto '{figura.nombre}' restaurado al paso {paso}.")

    elif op == "3":
        puntos = h.deshacer()
        escenario.reemplazar(figura.nombre, Figura(figura.nombre, puntos))
        print(f"  Ultima transformacion deshecha. '{figura.nombre}' "
              f"tiene ahora {len(puntos)} vertices.")


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
    print("=" * 58)

    escenario = Escenario()
    gestor = GestorHistorial()
    estado = {"ultimo": None}

    while True:
        print("\n" + SEP)
        print(f"Escenario: {len(escenario)} objeto(s)")
        print(escenario.listar())
        print(SEP)
        print("  1) Crear objeto (por coordenadas o por matriz)")
        print("  2) Ver detalle de un objeto")
        print("  3) Aplicar transformacion")
        print("  4) Analisis matematico del escenario")
        print("  5) Historial de transformaciones")
        print("  6) Ver grafico")
        print("  7) Eliminar un objeto")
        print("  0) Salir")

        op = leer_opcion("Opcion: ", {"0", "1", "2", "3", "4", "5", "6", "7"})
        if op == "0":
            print("Cerrando MathEngine 2D.")
            break
        elif op == "1":
            crear_objeto(escenario, gestor)
        elif op == "2":
            ver_objeto(escenario)
        elif op == "3":
            aplicar_transformacion(escenario, gestor, estado)
        elif op == "4":
            menu_analisis(escenario, gestor)
        elif op == "5":
            menu_historial(escenario, gestor)
        elif op == "6":
            ver_grafico(escenario, estado)
        elif op == "7":
            eliminar_objeto(escenario, gestor)


if __name__ == "__main__":
    main()