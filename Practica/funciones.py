import numpy as np

def row_echelon(A):
    """Return Row Echelon Form of matrix A."""
    A = A.copy()  # Trabajar sobre una copia de A
    r, c = A.shape
    
    if r == 0 or c == 0:
        return A

    for i in range(r):
        if A[i, 0] != 0:
            break
    else:
        B = row_echelon(A[:, 1:])
        return np.hstack([A[:, :1], B])

    if i > 0:
        A[[0, i]] = A[[i, 0]]  # Intercambiar filas

    A[0] = A[0] / A[0, 0]  # Normalizar la primera fila
    A[1:] -= A[0] * A[1:, 0:1]  # Eliminar la primera columna en las filas restantes

    B = row_echelon(A[1:, 1:])
    return np.vstack([A[:1], np.hstack([A[1:, :1], B])])

def row_echelon_augmented(A):
    """Return Row Echelon Form of an augmented matrix A and solve the system."""
    A = A.astype(float)  # Asegurarse de que trabajamos con floats
    r, c = A.shape
    
    for i in range(min(r, c-1)):
        # Seleccionar el pivote
        max_row = np.argmax(np.abs(A[i:, i])) + i
        A[[i, max_row]] = A[[max_row, i]]  # Intercambiar filas si es necesario

        # Si el pivote es 0, continuar con la siguiente columna
        if A[i, i] == 0:
            continue

        # Normalizar la fila con el pivote
        A[i] = A[i] / A[i, i]

        # Eliminar los elementos debajo del pivote
        for j in range(i+1, r):
            A[j] = A[j] - A[j, i] * A[i]
    
    # Volver hacia arriba para eliminar elementos sobre el pivote
    for i in range(min(r, c-1)-1, -1, -1):
        for j in range(i-1, -1, -1):
            A[j] = A[j] - A[j, i] * A[i]
    
    return A

def bashkara(a,b,c):
    """
    Genera las soluciones de la ecuación cuadrática ax^2+bx+c=0
    Args:
    a: coeficiente cuadrático
    b: coeficiente lineal
    c: término independiente
    Returns:
        x1: solución 1
        x2: solución 2
    """
    if a==0:
        return Exception("a no puede ser 0")
    
    return (-b+np.sqrt(b**2-4*a*c))/(2*a),(-b-np.sqrt(b**2-4*a*c))/(2*a)

def solve_linear_system(A_augmented):
    """Resuelve un sistema de ecuaciones lineales dado una matriz.
    Args:
        A_augmented: matriz aumentada del sistema de ecuaciones
    Returns:
        solution: solución del sistema de ecuaciones o None si no se puede resolver
    
    solution tiene la forma de un array de numpy con las soluciones de las incógnitas
    
    """
    # Separar la matriz de coeficientes (A) y el vector de términos independientes (b)
    A = A_augmented[:, :-1]  # Todas las columnas menos la última
    b = A_augmented[:, -1]   # Última columna
    
    # Resolver el sistema de ecuaciones
    try:
        solution = np.linalg.solve(A, b)
    except np.linalg.LinAlgError as e:
        print(f"Error: {e}")
        return None
    
    return solution

def traza(A: np.ndarray) -> int:
    """Calcula la traza de una matriz cuadrada.
    Args:
        A (np.ndarray): matriz cuadrada
    Returns:
        traza (int): traza de la matriz
    """
    resp = 0
    for i in range(len(A)):
        resp += A[i][i]
    ## 
    return resp

def sumamodulo(A: np.ndarray) -> int:
    """
    Suma los valores absolutos de los elementos de una matriz.
    Args:
        A (np.ndarray): matriz
    Returns:
        resp (int): suma de los valores absolutos de los elementos de la matriz
    """
    resp = 0
    for i in range(len(A)):
        for j in range(len(A[i])):
            resp += abs(A[i][j])
    ## 
    return resp

def positivosmayoresanegativos(A: np.ndarray) -> bool:
    """
    
    Args:
        A (np.ndarray): matriz
    Returns:
        resp (bool): True si la cantidad de números positivos es mayor a la cantidad de números negativos, False en caso contrario
    """
    resp = True
    positivos = 0
    negativos = 0
    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j] > 0:
                positivos += 1
            elif A[i][j] < 0:
                negativos += 1
    if positivos <= negativos:
        resp = False    
    ## 
    return resp

def escalonar_filas(M: np.ndarray) -> np.ndarray:
    """ 
        Retorna la Matriz Escalonada por Filas
        Args:
            M (np.ndarray): matriz
        Returns:
            np.ndarray: matriz escalonada por filas
    """
    A = np.copy(M)
    if (issubclass(A.dtype.type, np.integer)):
        A = A.astype(float)

    # Si A no tiene filas o columnas, ya esta escalonada
    f, c = A.shape
    if f == 0 or c == 0:
        return A

    # buscamos primer elemento no nulo de la primera columna
    i = 0
    
    while i < f and A[i,0] == 0:
        i += 1

    if i == f:
        # si todos los elementos de la primera columna son ceros
        # escalonamos filas desde la segunda columna
        B = escalonar_filas(A[:,1:])
        
        # y volvemos a agregar la primera columna de zeros
        return np.block([A[:,:1], B])


    # intercambiamos filas i <-> 0, pues el primer cero aparece en la fila i
    if i > 0:
        A[[0,i],:] = A[[i,0],:]

    # PASO DE TRIANGULACION GAUSSIANA:
    # a las filas subsiguientes les restamos un multiplo de la primera
    A[1:,:] -= (A[0,:] / A[0,0]) * A[1:,0:1]

    # escalonamos desde la segunda fila y segunda columna en adelante
    B = escalonar_filas(A[1:,1:])

    # reconstruimos la matriz por bloques adosando a B la primera fila 
    # y la primera columna (de ceros)
    return np.block([ [A[:1,:]], [ A[1:,:1], B] ])

