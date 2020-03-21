# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def extender(m):
    """
    Funcion para extender una matriz con el fin de poder aplicarle las reglas del juego de la vida.

    Parametros:
    ==============

    m: Matriz (NxN).

    Retorna:
    ==============

    m: Matriz extendida (N+2xN+2)
    """
    a, b = m.shape
    ex = np.zeros((a+2, b+2))
    
    ex[1:a+1, 1:b+1] = m

    return ex

def sumaVecinos(i, j, ex):
    """
    Funcion para calcular la suma de los vecinos de una celula, dada la posicion de la misma. \n
    Suma los valores en todas las direcciones.

    Parametros:
    ==============

    i: Fila. \n
    j: Columna. \n
    ex: Matriz extendida

    Retorna:
    ==============

    s: Numero que es la suma de todos los vecinos
    """
    s = (
        ex[i, j-1] + ex[i, j+1] + ex[i-1, j-1] + 
        (ex[i-1, j] + ex[i-1, j+1] + ex[i+1, j-1]) + 
        (ex[i+1, j]+ ex[i+1, j+1])
    )
    
    return s

def aplicarReglas(m):
    """
    Funcion para aplicar las reglas del juego de la vida a una matriz cualquiera.

    Parametros:
    ==============

    m: Matriz.

    Retorna:
    ==============

    nm: Nueva matriz con las reglas aplicadas
    """

    # dimension de matriz
    a, b = m.shape 

    # extiendo la matriz
    ex  = extender(m)

    # genero la nueva matriz
    nm = np.zeros((a, b), np.int)
    
    for i in range(1, a+1):
        for j in range(1, b+1):
            
            # calculo la suma de los vecinos
            s = sumaVecinos(i, j, ex)
            
            # aplico las reglas
            if(s > 3 or s <= 1): 
                nm[i-1, j-1] = 0
                
            if(s == 3 and m[i-1, j-1] == 0): 
                nm[i-1, j-1] = 1
                
            if((s == 3 or s == 2) and (m[i-1, j-1] == 1)): 
                nm[i-1, j-1] = 1

    return nm

def generarTablero(m):
    """
    Funcion que genera la grafica del tablero.

    Parametros:
    ==============

    m: Matriz a graficar.

    Retorna:
    ==============

    pieces: Grafica del tablero.
    """
    n = len(m)
    dx = 1/n
    pieces = []
    
    frame = patches.Rectangle((0.0, 0.0), 1, 1, fill=False, edgecolor="grey", linewidth=1) 
    pieces.append(frame)
    
    for j in range(n):
        for i in range(n):
            
            if m[i, j] == 1:
                
                p = patches.Rectangle((j/n, (n-1-i)/n), dx, dx, edgecolor="grey", facecolor="black", fill=True, linewidth=1)
                pieces.append(p)
                
            if m[i, j] == 0:
                
                p = patches.Rectangle((j/n, (n-1-i)/n), dx, dx, edgecolor="grey", fill=False, linewidth=1)
                pieces.append(p)
                
    return pieces

def mostrarTablero(x):
    """
    Funcion para mostrar el tablero correspondiente a una matriz.

    Parametros:
    ==============

    x: Tupla con el formato (matriz, nroEvolucion).

    Retorna:
    ==============

    void
    """

    ax1 = plt.subplot(111, aspect='equal')
    shape = generarTablero(x[0])
    
    for p in shape: 
        ax1.add_patch(p)
        
    plt.axis('on')
    plt.title('Evolucion ' + str(x[1]))
    plt.show()

def cargarMatriz(n):
    """
    Funcion para cargar una matriz de dimension NxN con un formato pre-diseñado.

    Parametros:
    ==============

    n: Dimension de la matriz (n >= 20).

    Retorna:
    ==============

    m: Matriz(NxN).
    """

    m = np.zeros((n, n), np.int)

    m[1,4] = 1
    m[1,5] = 1
    m[2,4] = 1
    m[3,4] = 1
    m[1,14] = 1
    m[1,15] = 1
    m[2,15] = 1
    m[3,15] = 1
    m[18,4] = 1
    m[18,5] = 1
    m[17,4] = 1
    m[15,4] = 1
    m[18,14] = 1
    m[18,15] = 1
    m[17,15] = 1
    m[16,15] = 1
    m[10, 4] = 1
    m[10, 5] = 1
    m[10, 6] = 1
    m[10, 7] = 1
    m[10, 8] = 1

    return m

def cargarMatrizRandom(n):
    """
    Funcion para cargar una matriz de dimension NxN con un formato random.

    Parametros:
    ==============

    n: Dimension de la matriz.

    Retorna:
    ==============

    m: Matriz(NxN).
    """

    m = np.random.randint(0, 2, (n,n))

    return m

def cortarMatriz(m, n):
    """
    Funcion para particionar la matriz en tantas partes como sea necesario
    para poder enviar las submatrices a cada procesador.

    Parametros:
    ==============

    m: Matriz a particionar. \n
    n: Cantidad de submatrices a formar, igual a la cantidad de procesos.

    Retorna:
    ==============

    v: Vector que contiene las submatrices.
    """

    # Divido la matriz en tantas partes como procesos haya y los guardo en a
    aux = np.split(m, n)

    # Hago una copia de la matriz a para poder trabajar mejor
    v = aux.copy()

    # A las sub matrices les asigno las filas de los bordes de las submatrices contiguas
    v[0] = np.concatenate((aux[0], aux[1][:1]))

    # Si hay solo 2 procesos este paso no es necesario
    # Este if se ejecuta para las partes que necesitan informacion superior e inferior
    if(n > 2):

        # A cada sub matriz interior le tengo que concatenar la parte inferior de la sub matriz
        # de arriba, y la parte superior de la sub matriz de abajo
        for i in range(1, n-1):

            x = aux[i-1].shape[0]
            v[i] = np.concatenate((aux[i-1][x-1:], aux[i], aux[i+1][:1]))
    
    # A la ultima sub matriz solo tengo que concatenarle la parte inferior de la sub matriz de arriba
    x = aux[n-2].shape[0]
    v[n-1] = np.concatenate((aux[n-2][x-1:], aux[n-1]))

    return v

def cortarExcedente(m, id, n):
    """
    Funcion para cortar la o las filas de referencia de una submatriz.

    Parametros:
    ==============

    m: Matriz a quitar excedente. \n
    id: ID del proceso activo. \n
    n: Cantidad de procesos.

    Retorna:
    ==============

    m: Matriz sin excedentes.
    """

    x = m.shape[0]
    # Si el proceso es el 0, corta la parte inferior
    if id == 0:
        return m[:x-1]

    # Si es el ultimo, corto la parte superior
    elif id == n-1:
        return m[1:] 

    # Si es uno del medio, corto la parte superior e inferior
    else:
        return m[1:x-1] 

def concatenarMatrices(v):
    """
    Funcion para unir/concatenar en conjuto de submatrices.

    Parametros:
    ==============

    v: Vector que contiene a las submatrices.

    Retorna:
    ==============

    m: Matriz (NxN).
    """

    m = v[0]
    
    for i in range(1, len(v)):
        m = np.concatenate((m, v[i]))
    
    return m


def unirMatriz(m, cantidadProcesos):
    """
    No se usa mas. Solo queda como un recuerdo de mi genialidad con los indices de las matrices.
    """

    # Vuelvo a iniciar la matriz original para cargarla con los nuevos valores
    init = np.zeros((20, 20), np.int)
    x = m[0].shape[0]
    init[:x-1] = m[0][:x-1]

    if(cantidadProcesos > 2):
        for i in range(1, cantidadProcesos-1):
            x = m[i].shape[0]
            init[(x-2)*i:(x-2)*i+(x-2)] = m[i][1:x-1]

    x = m[cantidadProcesos-1].shape[0]
    init[(x-1)*(cantidadProcesos-1):] = m[cantidadProcesos-1][1:]

    return init