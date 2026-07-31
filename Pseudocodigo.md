# Pseudocódigos de los algoritmos



## Convenciones utilizadas

Se emplea la notación de la Semana 3 del curso:

| Símbolo | Significado |
|---|---|
| `A ∈ M_{m×n}(ℝ)` | matriz de m filas y n columnas |
| `⟨A⟩_ij` | elemento de la fila i, columna j |
| `A_(i)` | i-ésima fila de A |
| `A^(j)` | j-ésima columna de A |
| `Aᵗ` | matriz transpuesta |

Todos los índices de este documento son **1-based**: el primer elemento de una matriz es `⟨A⟩_11` y no `⟨A⟩_00`, igual que en las diapositivas del curso. La implementación en Python trabaja internamente con índices 0-based y realiza la conversión al acceder a los elementos.

Los símbolos `←` (asignación) y `↔` (intercambio) se usan en el sentido habitual.

---

# 1. Núcleo de álgebra matricial

## 1.1 Crear una matriz

```
ALGORITMO CrearMatriz(datos)
    SI datos está vacío ENTONCES
        ERROR "una matriz necesita al menos una fila"
    FIN SI

    n ← cantidad de elementos de la primera fila

    PARA CADA fila EN datos HACER
        SI cantidad(fila) ≠ n ENTONCES
            ERROR "todas las filas deben tener la misma cantidad de columnas"
        FIN SI
        PARA CADA valor EN fila HACER
            SI valor no es un número real ENTONCES
                ERROR "valor no numérico"
            FIN SI
        FIN PARA
    FIN PARA

    m ← cantidad(datos)
    RETORNAR la matriz con esos datos, m filas y n columnas
FIN
```

## 1.2 Acceder a un elemento

```
ALGORITMO Elemento(A, i, j)                    // ⟨A⟩_ij
    SI i < 1 O i > m ENTONCES ERROR "fila fuera de rango" FIN SI
    SI j < 1 O j > n ENTONCES ERROR "columna fuera de rango" FIN SI
    RETORNAR datos[i][j]
FIN
```

## 1.3 Extraer una fila

```
ALGORITMO Fila(A, i)                           // A_(i), matriz de 1 × n
    SI i < 1 O i > m ENTONCES ERROR "fila fuera de rango" FIN SI
    RETORNAR una matriz nueva formada por la fila i de A
FIN
```

## 1.4 Extraer una columna

```
ALGORITMO Columna(A, j)                        // A^(j), matriz de m × 1
    SI j < 1 O j > n ENTONCES ERROR "columna fuera de rango" FIN SI
    CREAR C de tamaño m × 1
    PARA k DESDE 1 HASTA m HACER
        ⟨C⟩_k1 ← ⟨A⟩_kj
    FIN PARA
    RETORNAR C
FIN
```

## 1.5 Suma de matrices

```
ALGORITMO SumaMatrices(A, B)
    SI tamaño(A) ≠ tamaño(B) ENTONCES
        ERROR "la suma exige matrices del mismo tamaño"
    FIN SI
    CREAR C de tamaño m × n
    PARA i DESDE 1 HASTA m HACER
        PARA j DESDE 1 HASTA n HACER
            ⟨C⟩_ij ← ⟨A⟩_ij + ⟨B⟩_ij
        FIN PARA
    FIN PARA
    RETORNAR C
FIN
```

## 1.6 Producto por un escalar

```
ALGORITMO PorEscalar(λ, A)
    CREAR C de tamaño m × n
    PARA i DESDE 1 HASTA m HACER
        PARA j DESDE 1 HASTA n HACER
            ⟨C⟩_ij ← λ · ⟨A⟩_ij
        FIN PARA
    FIN PARA
    RETORNAR C
FIN
```

## 1.7 Resta de matrices

```
ALGORITMO Resta(A, B)
    RETORNAR SumaMatrices(A, PorEscalar(−1, B))    // A − B = A + (−1·B)
FIN
```

## 1.8 Producto de matrices

```
ALGORITMO ProductoMatrices(A, B)
    // A es m × n,  B es n × h,  el resultado es m × h
    SI columnas(A) ≠ filas(B) ENTONCES
        ERROR "producto no definido"
    FIN SI

    CREAR C de tamaño m × h
    PARA i DESDE 1 HASTA m HACER              // filas de A
        PARA j DESDE 1 HASTA h HACER          // columnas de B
            acumulado ← 0
            PARA k DESDE 1 HASTA n HACER      // recorre fila i y columna j
                acumulado ← acumulado + ⟨A⟩_ik · ⟨B⟩_kj
            FIN PARA
            ⟨C⟩_ij ← acumulado
        FIN PARA
    FIN PARA
    RETORNAR C
FIN
```

## 1.9 Desarrollo escrito del producto

```
ALGORITMO DetalleProducto(A, B)
    SI columnas(A) ≠ filas(B) ENTONCES
        ERROR "producto no definido"
    FIN SI

    líneas ← lista vacía
    PARA i DESDE 1 HASTA m HACER
        PARA j DESDE 1 HASTA h HACER
            texto ← "⟨C⟩_ij = "
            PARA k DESDE 1 HASTA n HACER
                agregar a texto:  ⟨A⟩_ik "*" ⟨B⟩_kj
                SI k < n ENTONCES agregar " + " FIN SI
            FIN PARA
            agregar a texto:  " = " valor de ⟨C⟩_ij
            AGREGAR texto A líneas
        FIN PARA
    FIN PARA
    RETORNAR líneas
FIN
```

## 1.10 Transpuesta

```
ALGORITMO Transpuesta(A)                       // ⟨Aᵗ⟩_ij = ⟨A⟩_ji
    CREAR T de tamaño n × m
    PARA i DESDE 1 HASTA m HACER
        PARA j DESDE 1 HASTA n HACER
            ⟨T⟩_ji ← ⟨A⟩_ij
        FIN PARA
    FIN PARA
    RETORNAR T
FIN
```

## 1.11 Igualdad de matrices

```
ALGORITMO SonIguales(A, B)
    SI tamaño(A) ≠ tamaño(B) ENTONCES RETORNAR FALSO FIN SI
    PARA i DESDE 1 HASTA m HACER
        PARA j DESDE 1 HASTA n HACER
            SI |⟨A⟩_ij − ⟨B⟩_ij| ≥ TOLERANCIA ENTONCES
                RETORNAR FALSO
            FIN SI
        FIN PARA
    FIN PARA
    RETORNAR VERDADERO
FIN
```

## 1.12 Criterios de clasificación

```
EsCuadrada(A)            : m = n
EsMatrizFila(A)          : m = 1
EsMatrizColumna(A)       : n = 1
EsNula(A)                : ⟨A⟩_ij = 0 para todo i, j
EsDiagonal(A)            : A es cuadrada Y ⟨A⟩_ij = 0 para todo i ≠ j
EsIdentidad(A)           : A es cuadrada Y ⟨A⟩_ij = 1 si i = j, 0 si i ≠ j
EsTriangularSuperior(A)  : A es cuadrada Y ⟨A⟩_ij = 0 para todo i > j
EsTriangularInferior(A)  : A es cuadrada Y ⟨A⟩_ij = 0 para todo i < j
```

## 1.13 Clasificar una matriz

```
ALGORITMO Clasificar(A)
    tipos ← lista vacía

    SI EsCuadrada(A) ENTONCES agregar "cuadrada de orden m" FIN SI
    SI EsMatrizFila(A) ENTONCES agregar "matriz fila" FIN SI
    SI EsMatrizColumna(A) ENTONCES agregar "matriz columna (vector)" FIN SI
    SI EsNula(A) ENTONCES agregar "matriz nula" FIN SI

    SI EsIdentidad(A) ENTONCES
        agregar "matriz identidad"
    SINO SI EsDiagonal(A) ENTONCES
        agregar "matriz diagonal"
    FIN SI

    SI EsTriangularSuperior(A) Y NO EsDiagonal(A) ENTONCES
        agregar "triangular superior"
    FIN SI
    SI EsTriangularInferior(A) Y NO EsDiagonal(A) ENTONCES
        agregar "triangular inferior"
    FIN SI

    SI tipos está vacío ENTONCES
        agregar "matriz de m×n sin tipo especial"
    FIN SI
    RETORNAR tipos
FIN
```

---

# 2. Actividad #1 — Representación de objetos

## 2.1 Validar los vértices

```
ALGORITMO ValidarVértices(vértices)
    SI vértices está vacío ENTONCES
        ERROR "debe indicar al menos un vértice"
    FIN SI

    limpios ← lista vacía
    PARA CADA (k, p) EN vértices HACER
        SI p no es un par ordenado ENTONCES
            ERROR "el vértice k debe ser un par (x, y)"
        FIN SI
        SI x o y no son números reales ENTONCES
            ERROR "coordenada no numérica en el vértice k"
        FIN SI
        AGREGAR (x, y) A limpios
    FIN PARA

    PARA k DESDE 1 HASTA cantidad(limpios) − 1 HACER
        SI limpios[k] = limpios[k+1] ENTONCES
            ERROR "los vértices k y k+1 son iguales"
        FIN SI
    FIN PARA

    RETORNAR limpios
FIN
```

## 2.2 Crear una figura

```
ALGORITMO CrearFigura(nombre, vértices)
    SI nombre está vacío ENTONCES
        ERROR "el objeto debe tener un nombre"
    FIN SI

    vértices ← ValidarVértices(vértices)
    n ← cantidad(vértices)

    CREAR A de tamaño 2 × n
    PARA j DESDE 1 HASTA n HACER
        ⟨A⟩_1j ← componente x del vértice j        // fila de abscisas
        ⟨A⟩_2j ← componente y del vértice j        // fila de ordenadas
    FIN PARA

    RETORNAR la figura con ese nombre y esa matriz
FIN
```

## 2.3 Reconstruir una figura desde su matriz

```
ALGORITMO FiguraDesdeMatriz(nombre, A)
    // Admite dos representaciones:
    //   2 filas -> cartesiana:  columna j = (xj, yj)
    //   3 filas -> homogénea:   columna j = (xj, yj, wj)

    SI filas(A) = 2 ENTONCES
        puntos ← lista vacía
        PARA j DESDE 1 HASTA columnas(A) HACER
            AGREGAR (⟨A⟩_1j , ⟨A⟩_2j) A puntos
        FIN PARA
        RETORNAR CrearFigura(nombre, puntos)
    FIN SI

    SI filas(A) = 3 ENTONCES
        puntos ← lista vacía
        PARA j DESDE 1 HASTA columnas(A) HACER
            w ← ⟨A⟩_3j
            SI |w| < TOLERANCIA ENTONCES
                ERROR "la columna j tiene w = 0: es un punto en el infinito"
            FIN SI
            AGREGAR (⟨A⟩_1j / w , ⟨A⟩_2j / w) A puntos
        FIN PARA
        RETORNAR CrearFigura(nombre, puntos)
    FIN SI

    ERROR "la matriz debe tener 2 o 3 filas"
FIN
```

## 2.4 Obtener la matriz homogénea de una figura

```
ALGORITMO MatrizHomogénea(figura)
    // Agrega una tercera fila constante igual a 1:
    //
    //         | x1  x2  ...  xn |
    //   A_h = | y1  y2  ...  yn |
    //         |  1   1  ...   1 |

    A ← matriz de la figura                    // de tamaño 2 × n
    CREAR H de tamaño 3 × columnas(A)
    PARA j DESDE 1 HASTA columnas(A) HACER
        ⟨H⟩_1j ← ⟨A⟩_1j
        ⟨H⟩_2j ← ⟨A⟩_2j
        ⟨H⟩_3j ← 1
    FIN PARA
    RETORNAR H
FIN
```

## 2.5 Obtener el vector de posición de un vértice

```
ALGORITMO VectorPosición(figura, j)            // matriz columna de 2 × 1
    RETORNAR Columna(matriz de la figura, j)
FIN

ALGORITMO VectorPosiciónHomogéneo(figura, j)   // matriz columna de 3 × 1
    RETORNAR Columna(MatrizHomogénea(figura), j)
FIN
```

## 2.6 Agregar un objeto al escenario

```
ALGORITMO Agregar(escenario, figura)
    SI ya existe un objeto con ese nombre ENTONCES
        ERROR "nombre duplicado"
    FIN SI
    AGREGAR figura A escenario.objetos
FIN
```

## 2.7 Obtener un objeto del escenario

```
ALGORITMO Obtener(escenario, nombre)
    PARA CADA objeto EN escenario.objetos HACER
        SI normalizar(objeto.nombre) = normalizar(nombre) ENTONCES
            RETORNAR objeto
        FIN SI
    FIN PARA
    ERROR "no existe un objeto con ese nombre"
FIN
```

## 2.8 Reemplazar un objeto del escenario

```
ALGORITMO Reemplazar(escenario, nombre, figura_nueva)
    objeto   ← Obtener(escenario, nombre)
    posición ← índice de objeto en la lista
    escenario.objetos[posición] ← figura_nueva
FIN
```

---

# 3. Actividad #2 — Transformaciones geométricas

## 3.1 Matriz de rotación

```
ALGORITMO MatrizRotación(θ_grados)
    θ ← θ_grados · π / 180
    RETORNAR  | cos θ   −sen θ |
              | sen θ    cos θ |
FIN
```

## 3.2 Matriz de escalamiento

```
ALGORITMO MatrizEscalamiento(sx, sy)
    SI sy no se indicó ENTONCES sy ← sx FIN SI        // escalamiento uniforme
    SI |sx| < TOLERANCIA O |sy| < TOLERANCIA ENTONCES
        ERROR "un factor 0 colapsa la figura y la transformación no es reversible"
    FIN SI
    RETORNAR  | sx   0 |
              |  0  sy |
FIN
```

## 3.3 Matriz de reflexión

```
ALGORITMO MatrizReflexión(eje)
    SEGÚN eje HACER
        "x"      : RETORNAR |  1   0 ;  0  −1 |
        "y"      : RETORNAR | −1   0 ;  0   1 |
        "origen" : RETORNAR | −1   0 ;  0  −1 |
        "y=x"    : RETORNAR |  0   1 ;  1   0 |
        "y=-x"   : RETORNAR |  0  −1 ; −1   0 |
        SINO     : ERROR "eje no válido"
    FIN SEGÚN
FIN
```

## 3.4 Matriz de traslación

```
ALGORITMO MatrizTraslación(tx, ty, n)
    CREAR T de tamaño 2 × n
    PARA j DESDE 1 HASTA n HACER
        ⟨T⟩_1j ← tx
        ⟨T⟩_2j ← ty
    FIN PARA
    RETORNAR T
FIN
```

## 3.5 Aplicar una transformación lineal

```
ALGORITMO AplicarLineal(figura, M, descripción)
    A  ← matriz de la figura
    A' ← ProductoMatrices(M, A)                    // A' = M · A

    cálculos ← ["A' = M · A   (2×2)·(2×n) = (2×n)"]
    cálculos ← cálculos + DetalleProducto(M, A)

    RETORNAR Resultado(descripción, "producto", M,
                       figura, FiguraDesdeMatriz(nombre, A'), cálculos)
FIN
```

## 3.6 Trasladar una figura

```
ALGORITMO Trasladar(figura, tx, ty)
    A  ← matriz de la figura
    T  ← MatrizTraslación(tx, ty, columnas(A))
    A' ← SumaMatrices(A, T)                        // A' = A + T

    cálculos ← ["A' = A + T   (suma de matrices de 2×n)"]
    PARA j DESDE 1 HASTA columnas(A) HACER
        agregar:  "Pj' = (xj + tx, yj + ty) = (xj', yj')"
    FIN PARA

    RETORNAR Resultado("Traslación por (tx, ty)", "suma", T,
                       figura, FiguraDesdeMatriz(nombre, A'), cálculos)
FIN
```

## 3.7 Transformar respecto a un punto distinto del origen

```
ALGORITMO RespectoACentro(figura, M, C, descripción)
    // A' = M · (A − C) + C

    paso1 ← Trasladar(figura, −Cx, −Cy)             // lleva C al origen
    paso2 ← AplicarLineal(paso1.resultado, M, ...)  // aplica la matriz
    paso3 ← Trasladar(paso2.resultado, Cx, Cy)      // devuelve la figura

    cálculos ← encabezado + cálculos de los tres pasos

    RETORNAR Resultado(descripción, "compuesta", M,
                       figura, paso3.resultado, cálculos)
FIN
```

## 3.8 Aplicar transformaciones consecutivas

```
ALGORITMO AplicarSecuencia(figura, operaciones)
    actual     ← figura
    resultados ← lista vacía

    PARA CADA op EN operaciones HACER
        SEGÚN op.tipo HACER
            "rotar"     : r ← Rotar(actual, op.ángulo)
            "escalar"   : r ← Escalar(actual, op.factores)
            "reflejar"  : r ← Reflejar(actual, op.eje)
            "trasladar" : r ← Trasladar(actual, op.tx, op.ty)
            SINO        : ERROR "operación desconocida"
        FIN SEGÚN

        AGREGAR r A resultados
        actual ← r.figura_resultante                // encadena los pasos
    FIN PARA

    RETORNAR actual, resultados
FIN
```

## 3.9 Calcular la matriz compuesta

```
ALGORITMO MatrizCompuesta(M1, M2, ..., Mk)
    // Solo válido para transformaciones LINEALES.
    // Resultado:  M = Mk · … · M2 · M1

    M ← I₂                                          // identidad de orden 2
    PARA i DESDE 1 HASTA k HACER
        M ← ProductoMatrices(Mi, M)                 // Mi por la izquierda
    FIN PARA
    RETORNAR M
FIN
```

---

# 4. Actividad #2 — Coordenadas homogéneas

## 4.1 Convertir una matriz lineal a su forma homogénea

```
ALGORITMO AHomogénea(M)
    // | a  b |         | a  b  0 |
    // | c  d |   -->   | c  d  0 |
    //                  | 0  0  1 |

    SI tamaño(M) ≠ (2, 2) ENTONCES
        ERROR "se esperaba una matriz de 2 × 2"
    FIN SI

    CREAR H de tamaño 3 × 3
    ⟨H⟩_11 ← ⟨M⟩_11   ;  ⟨H⟩_12 ← ⟨M⟩_12   ;  ⟨H⟩_13 ← 0
    ⟨H⟩_21 ← ⟨M⟩_21   ;  ⟨H⟩_22 ← ⟨M⟩_22   ;  ⟨H⟩_23 ← 0
    ⟨H⟩_31 ← 0        ;  ⟨H⟩_32 ← 0        ;  ⟨H⟩_33 ← 1
    RETORNAR H
FIN
```

## 4.2 Matrices homogéneas de las transformaciones lineales

```
ALGORITMO MatrizRotaciónH(θ_grados)
    RETORNAR AHomogénea(MatrizRotación(θ_grados))
FIN

ALGORITMO MatrizEscalamientoH(sx, sy)
    RETORNAR AHomogénea(MatrizEscalamiento(sx, sy))
FIN

ALGORITMO MatrizReflexiónH(eje)
    RETORNAR AHomogénea(MatrizReflexión(eje))
FIN
```

## 4.3 Matriz homogénea de traslación

```
ALGORITMO MatrizTraslaciónH(tx, ty)
    // A diferencia de la versión cartesiana, esta matriz es de 3 × 3 y no
    // depende de la cantidad de vértices de la figura.

    RETORNAR  | 1  0  tx |
              | 0  1  ty |
              | 0  0   1 |
FIN
```

## 4.4 Construir la matriz homogénea de una operación

```
ALGORITMO MatrizTransformaciónH(operación)
    SEGÚN operación.tipo HACER
        "rotar"     : RETORNAR MatrizRotaciónH(operación.ángulo)
        "escalar"   : RETORNAR MatrizEscalamientoH(operación.factores)
        "reflejar"  : RETORNAR MatrizReflexiónH(operación.eje)
        "trasladar" : RETORNAR MatrizTraslaciónH(operación.tx, operación.ty)
        SINO        : ERROR "operación desconocida"
    FIN SEGÚN
FIN
```

## 4.5 Matriz compuesta homogénea

```
ALGORITMO MatrizCompuestaH(M1, M2, ..., Mk)
    // A diferencia de MatrizCompuesta, esta versión SÍ admite traslaciones,
    // porque en coordenadas homogéneas también son productos.

    M ← I₃                                          // identidad de orden 3
    PARA i DESDE 1 HASTA k HACER
        SI tamaño(Mi) ≠ (3, 3) ENTONCES
            ERROR "todas las matrices deben ser de 3 × 3"
        FIN SI
        M ← ProductoMatrices(Mi, M)                 // Mi por la izquierda
    FIN PARA
    RETORNAR M
FIN
```

## 4.6 Aplicar una transformación homogénea

```
ALGORITMO AplicarHomogénea(figura, H, descripción)
    SI tamaño(H) ≠ (3, 3) ENTONCES
        ERROR "se esperaba una matriz de 3 × 3"
    FIN SI

    A_h  ← MatrizHomogénea(figura)                 // 3 × n
    A_h' ← ProductoMatrices(H, A_h)                // A_h' = H · A_h

    cálculos ← ["A_h' = H · A_h   (3×3)·(3×n) = (3×n)"]
    cálculos ← cálculos + DetalleProducto(H, A_h)

    RETORNAR Resultado(descripción, "homogénea", H,
                       figura, FiguraDesdeMatriz(nombre, A_h'), cálculos)
FIN
```

## 4.7 Aplicar una secuencia con una sola matriz

```
ALGORITMO AplicarSecuenciaHomogénea(figura, operaciones)
    SI operaciones está vacío ENTONCES
        ERROR "debe indicar al menos una transformación"
    FIN SI

    matrices ← lista vacía
    PARA CADA op EN operaciones HACER
        AGREGAR MatrizTransformaciónH(op) A matrices
    FIN PARA

    H_total   ← MatrizCompuestaH(matrices)
    resultado ← AplicarHomogénea(figura, H_total, descripción)

    RETORNAR resultado.figura_resultante, H_total, resultado, matrices
FIN
```

---

# 5. Actividad #3 — Análisis matemático del escenario

## 5.1 Reducción de Gauss-Jordan

```
ALGORITMO GaussJordan(A)
    R           ← copia de A          // no se modifica el original
    pivotes     ← lista vacía
    pasos       ← lista vacía
    fila_actual ← 1

    PARA col DESDE 1 HASTA n HACER
        SI fila_actual > m ENTONCES SALIR FIN SI

        // 1) Elección del pivote de mayor valor absoluto
        mejor ← fila_actual
        PARA i DESDE fila_actual+1 HASTA m HACER
            SI |⟨R⟩_i,col| > |⟨R⟩_mejor,col| ENTONCES mejor ← i FIN SI
        FIN PARA

        SI |⟨R⟩_mejor,col| < TOLERANCIA ENTONCES
            CONTINUAR      // columna sin pivote → variable libre
        FIN SI

        // 2) Intercambio
        SI mejor ≠ fila_actual ENTONCES
            INTERCAMBIAR R_(fila_actual) ↔ R_(mejor)
            registrar paso "F_fila_actual ↔ F_mejor"
        FIN SI

        // 3) Normalización del pivote a 1
        p ← ⟨R⟩_fila_actual,col
        SI p ≠ 1 ENTONCES
            R_(fila_actual) ← (1/p) · R_(fila_actual)
            registrar paso "F_fila_actual ← (1/p) F_fila_actual"
        FIN SI

        // 4) Eliminación del resto de la columna, arriba y abajo
        PARA i DESDE 1 HASTA m HACER
            SI i ≠ fila_actual ENTONCES
                c ← ⟨R⟩_i,col
                SI c ≠ 0 ENTONCES
                    R_(i) ← R_(i) − c · R_(fila_actual)
                    registrar paso "F_i ← F_i − (c) F_fila_actual"
                FIN SI
            FIN SI
        FIN PARA

        AGREGAR col A pivotes
        fila_actual ← fila_actual + 1
    FIN PARA

    // Limpieza de residuos de punto flotante
    PARA CADA ⟨R⟩_ij HACER
        SI |⟨R⟩_ij| < TOLERANCIA ENTONCES ⟨R⟩_ij ← 0 FIN SI
    FIN PARA

    RETORNAR R, pivotes, pasos
FIN
```

## 5.2 Rango de una matriz

```
ALGORITMO Rango(A)
    R, pivotes ← GaussJordan(A)
    RETORNAR cantidad(pivotes)
FIN
```

## 5.3 Armar la matriz de un conjunto de vectores

```
ALGORITMO MatrizDeVectores(v1, v2, ..., vk)
    // Los vectores se colocan como COLUMNAS
    dim ← cantidad de componentes de v1
    SI algún vector tiene distinta cantidad de componentes ENTONCES
        ERROR "los vectores deben tener la misma dimensión"
    FIN SI
    CREAR A de tamaño dim × k
    PARA j DESDE 1 HASTA k HACER
        A^(j) ← vj
    FIN PARA
    RETORNAR A
FIN
```

## 5.4 Analizar independencia lineal, base y dimensión

```
ALGORITMO AnalizarConjunto(v1, v2, ..., vk)
    A ← MatrizDeVectores(v1, ..., vk)
    R, pivotes, pasos ← GaussJordan(A)
    libres ← columnas de A que NO son pivote

    independiente ← (cantidad(pivotes) = k)
    base          ← { vj : j ∈ pivotes }
    dimensión     ← cantidad(pivotes)

    // Los coeficientes de cada combinación lineal se leen directamente en
    // la matriz escalonada reducida
    combinaciones ← diccionario vacío
    PARA CADA j EN libres HACER
        expresión ← ""
        PARA r DESDE 1 HASTA cantidad(pivotes) HACER
            coef ← ⟨R⟩_r,j
            SI coef ≠ 0 ENTONCES
                agregar a expresión:  "(coef) · v_{pivotes[r]}"
            FIN SI
        FIN PARA
        SI expresión está vacía ENTONCES
            expresión ← "0"        // vj es el vector nulo
        FIN SI
        combinaciones[vj] ← expresión
    FIN PARA

    RETORNAR independiente, base, dimensión, combinaciones, R, pasos
FIN
```

## 5.5 Detectar vértices redundantes

```
ALGORITMO VérticesRedundantes(figura, cerrada)
    P ← lista de vértices
    n ← cantidad(P)

    SI n < 3 ENTONCES
        RETORNAR (ninguno, P)
    FIN SI

    redundantes ← lista vacía
    PARA k DESDE 1 HASTA n HACER
        SI NO cerrada Y (k = 1 O k = n) ENTONCES
            CONTINUAR      // los extremos de una polilínea nunca sobran
        FIN SI

        anterior  ← P[((k−2) mod n) + 1]
        siguiente ← P[(k mod n) + 1]

        u ← P[k] − anterior            // vector de arista entrante
        w ← siguiente − P[k]           // vector de arista saliente

        M ← matriz 2×2 cuyas columnas son u y w
        SI Rango(M) < 2 ENTONCES       // u y w linealmente dependientes
            AGREGAR k A redundantes
        FIN SI
    FIN PARA

    optimizada ← { P[k] : k ∉ redundantes }
    RETORNAR redundantes, optimizada
FIN
```

## 5.6 Verificar si un conjunto es subespacio vectorial

```
ALGORITMO EsSubespacio(a, b, c)
    // Analiza W = { (x,y) ∈ ℝ² : a·x + b·y = c }

    SI a = 0 Y b = 0 ENTONCES
        ERROR "la condición no define una recta"
    FIN SI

    // Elección de dos puntos concretos de W
    SI c = 0 ENTONCES
        u ← (−b, a)                        // vector director
        v ← (−2b, 2a)
    SINO SI a = 0 ENTONCES                 // recta horizontal y = c/b
        u ← (0, c/b)  ;  v ← (1, c/b)
    SINO SI b = 0 ENTONCES                 // recta vertical x = c/a
        u ← (c/a, 0)  ;  v ← (c/a, 1)
    SINO                                   // cortes con los ejes
        u ← (c/a, 0)  ;  v ← (0, c/b)
    FIN SI

    DEFINIR evaluar(p) COMO  a·px + b·py

    // Condición 1: el vector nulo pertenece a W
    cumple_nulo ← (0 = c)

    // Condición 2: cierre bajo la suma
    s ← u + v
    cumple_suma ← (evaluar(s) = c)

    // Condición 3: cierre bajo el producto por un escalar
    λ ← 2
    e ← λ·u
    cumple_escalar ← (evaluar(e) = c)

    RETORNAR cumple_nulo Y cumple_suma Y cumple_escalar
FIN
```

---

# 6. Actividad #4 — Historial de transformaciones

## 6.1 Estructuras de datos

```
ESTRUCTURA Registro
    numero        : posición en el historial, empezando en 1
    descripción   : texto legible, "Rotación de 45 grados"
    operación     : "producto" | "suma" | "compuesta" | "homogénea" | "estructural"
    matriz_usada  : la matriz aplicada, o VACÍO si no hubo
    antes         : coordenadas previas
    después       : coordenadas resultantes
FIN

ESTRUCTURA Historial
    nombre_objeto   : a qué objeto pertenece
    estado_inicial  : coordenadas al momento de crearse
    registros       : PILA de registros
FIN

ESTRUCTURA GestorHistorial
    historiales : diccionario  nombre_normalizado → Historial
FIN
```

## 6.2 Símbolo de la operación

```
ALGORITMO Símbolo(registro)
    SEGÚN registro.operación HACER
        "producto"   : RETORNAR "A' = M · A"
        "suma"       : RETORNAR "A' = A + T"
        "compuesta"  : RETORNAR "A' = M · (A − C) + C"
        "homogénea"  : RETORNAR "A_h' = H · A_h"
        SINO         : RETORNAR "modificación estructural"
    FIN SEGÚN
FIN
```

## 6.3 Registrar una transformación

```
ALGORITMO Registrar(historial, resultado)
    r ← nuevo Registro con:
        numero       ← cantidad(historial.registros) + 1
        descripción  ← resultado.descripción
        operación    ← resultado.operación
        matriz_usada ← resultado.matriz_usada
        antes        ← vértices de resultado.figura_antes
        después      ← vértices de resultado.figura_después

    APILAR r EN historial.registros
    RETORNAR r
FIN
```

## 6.4 Registrar una modificación no matricial

```
ALGORITMO RegistrarEvento(historial, descripción, antes, después)
    r ← nuevo Registro con operación = "estructural" y matriz_usada = VACÍO
    APILAR r EN historial.registros
    RETORNAR r
FIN
```

## 6.5 Reconstruir un estado anterior

```
ALGORITMO Reconstruir(historial, paso)
    SI paso < 0 O paso > cantidad(historial.registros) ENTONCES
        ERROR "paso fuera de rango"
    FIN SI
    SI paso = 0 ENTONCES
        RETORNAR historial.estado_inicial
    FIN SI
    RETORNAR historial.registros[paso].después
FIN
```

## 6.6 Deshacer la última transformación

```
ALGORITMO Deshacer(historial)
    SI historial.registros está vacío ENTONCES
        RETORNAR historial.estado_inicial
    FIN SI
    r ← DESAPILAR historial.registros
    RETORNAR r.antes
FIN
```

## 6.7 Iniciar el historial de un objeto

```
ALGORITMO Iniciar(gestor, figura)
    gestor.historiales[normalizar(figura.nombre)] ←
        nuevo Historial(figura.nombre, figura.vértices)
FIN
```

## 6.8 Asegurar la existencia de un historial

```
ALGORITMO Asegurar(gestor, nombre, vértices_iniciales)
    SI normalizar(nombre) ∉ gestor.historiales ENTONCES
        gestor.historiales[normalizar(nombre)] ←
            nuevo Historial(nombre, vértices_iniciales)
    FIN SI
    RETORNAR gestor.historiales[normalizar(nombre)]
FIN
```

## 6.9 Registrar una secuencia de transformaciones

```
ALGORITMO RegistrarSecuencia(gestor, destino, figura_origen, resultados)
    h ← Asegurar(gestor, destino, figura_origen.vértices)
    PARA CADA r EN resultados HACER
        Registrar(h, r)
    FIN PARA
    RETORNAR h
FIN
```

## 6.10 Mostrar la cadena de transformaciones

```
ALGORITMO Cadena(historial)
    pasos ← [ "nombre_objeto creada (n vértices)" ]
    PARA CADA r EN historial.registros HACER
        AGREGAR r.descripción A pasos
    FIN PARA
    RETORNAR pasos unidos por  "\n   |\n   v\n"
FIN
```

---

## Fuentes

Paez, C. (2013). *Matrices y Sistemas* (1.ª ed.).