# Imports
import numpy as np
import random
import matplotlib.pyplot as plt


# CONSTANTES
reinas = 16
porcentajeMutacion = 0.05
porcentajeCruza = 0.5


def aptitud(v):
    """
    Funcion para calcular la aptitud o fitness de un individuo, contando tanto los ataques en diagonal
    como ataques horizontales.

    Parametros:
    ==============

    v: Vector individuo ([x,x,x,...]).

    Retorna:
    ==============

    s: Cantidad de ataques entre las reinas del individuo.
    """
    
    size = len(v)
    
    # Los ataques sólo pueden ser en las diagonales
    diagonal_izquierda_derecha = [0] * (2*size-1)
    diagonal_derecha_izquierda = [0] * (2*size-1)
    horizontal = [0] * size
    
    # Número de reinas en cada diagonal
    for i in range(size): # recorremos las columnas
        diagonal_izquierda_derecha[i+v[i]] += 1 # [columna + fila]
        diagonal_derecha_izquierda[size-1-i+v[i]] += 1 # [size-1-columna+ fila]
        horizontal[v[i]] += 1 
    
    # Número de ataques en cada diagonal
    s = 0
    for i in range(2*size-1): # recorremos todas las diagonales
        if diagonal_izquierda_derecha[i] > 1: # hay ataques
            s += diagonal_izquierda_derecha[i] - 1 # n-1 ataques
        if diagonal_derecha_izquierda[i] > 1:
            s += diagonal_derecha_izquierda[i] - 1
    
    # Numero de ataques en las horizontales
    for i in range(size):
        if horizontal[i] > 1:
            s += horizontal[i]

    return s

def cruzar(p, m):
    """
    Funcion para cruzar dos individuos, mediante un corte aleatorio generando dos hijos.

    Parametros:
    ==============

    p: Vector padre. \n
    m: Vector madre.

    Retorna:
    ==============

    h1: Primer hijo. \n
    h2: Segundo hijo.
    """
    
    corte = random.randint(1, reinas-2)
    
    h1 = p[corte:] + m[:corte]
    h2 = m[corte:] + p[:corte]
    
    return h1, h2

def mutacion(v):
    """
    Funcion para mutar un individuo, cada individuo tiene una probabilidad de mutar, 
    por lo que puede suceder o no.

    Parametros:
    ==============

    v: Vector individuo.

    Retorna:
    ==============

    v: Vector individuo.
    """
    
    # muto?
    m = random.random()
    
    if(m < porcentajeMutacion):
        
        columna = random.randint(0, reinas-1)
        
        fila = random.randint(0, reinas-1)
        
        while(fila == v[columna]):
            fila = random.randint(0, reinas-1)

        v[columna] = fila
    
    return v

def individuoRandom():
    """
    Funcion para crear un vector individuo aleatorio.

    Parametros:
    ==============

    None.

    Retorna:
    ==============

    v: Vector individuo.
    """

    v = []
    
    for i in range(reinas):
    
        fila = random.randint(0, reinas-1)
        
        v.append(fila)
    
    return v

def obtenerAptitud(v):
    """
    Funcion para retornar el fitness o aptitud de un individuo.

    Parametros:
    ==============

    v: Tupla (individuo: vector, fitness: int).

    Retorna:
    ==============

    v[1]: Aptitud del individuo.
    """

    return v[1]

def cruzaYMutacion(p):
    """
    Funcion para realizar las cruzas y mutaciones de una poblacion.

    Parametros:
    ==============

    p: Vector de poblacion.

    Retorna:
    ==============

    p: Vector de poblacion mas hijos nuevos.
    """
    
    for i in range(len(p)):
        
            c = random.random()
            # cruzo?
            if(c < porcentajeCruza):
                
                # selecciono un padre y una madre al azar
                padre = random.randint(0, len(p)-1)
                madre = random.randint(0, len(p)-1)

                # hago la cruza
                h1, h2 = cruzar(p[padre][0], p[madre][0])

                # hago la mutacion
                h1 = mutacion(h1)
                h2 = mutacion(h2)
                
                # agrego los hijos a la poblacion con su respectivo fitness
                ind1 = []
                ind1.append(h1)
                ind1.append(aptitud(h1))

                ind2 = []
                ind2.append(h2)
                ind2.append(aptitud(h2))
                
                p.append(ind1)
                p.append(ind2)

    return p

def imprimirTablero(v):
    """
    Funcion para graficar el tablero de un individuo.

    Parametros:
    ==============

    v: Tupla (individuo: vector, fitness: int).

    Retorna:
    ==============

    Void.
    """
    
    x = range(len(v[0]))
    x = np.array(x)
    
    y = np.array(v[0])
    
    x = x + 0.5
    y = y + 0.5
    plt.figure()
    plt.scatter(x, y)
    plt.xlim(0, reinas)
    plt.ylim(0, reinas)
    plt.xticks(x-0.5)
    plt.yticks(x-0.5)
    plt.grid(True)
    plt.title("Individuo " + str(v[0]) + " - Ataques: " + str(v[1]))
    plt.show()

def dividirPoblacion(p, t):
    """
    Funcion para dividir una poblacion en sub poblaciones.

    Parametros:
    ==============

    p: Poblacion de individuos \n
    t: Cantidad de individuos por sub poblacion.

    Retorna:
    ==============

    v: Vector que contiene en cada posicion a una sub poblacion.
    """

    v = []
    for i in range(0, len(p), t):
        v.append(p[i:i+t])
    
    return v

def unirPoblacion(v):
    """
    Funcion para unir un vector de sub poblaciones en una sola pobacion.

    Parametros:
    ==============

    v: Vector con sub poblacion.

    Retorna:
    ==============

    p: Vector de poblacion/individuos.
    """

    p = []

    for i in range(len(v)):

        for j in range(len(v[i])):

            p.append(v[i][j])
    
    return p

def aptitudPromedio(v):
    """
    Funcion para calcular la aptitud o fitness promedio de una poblacion.

    Parametros:
    ==============

    v: Vector de poblacion/individuos.

    Retorna:
    ==============

    p: Aptitud promedio.
    """

    ac = 0

    for i in range(len(v)):
        ac += v[i][1]
    
    p = ac/len(v)

    return p

def aptitudMinima(p):
    """
    Funcion para calcular la aptitud o fitness minimo de una poblacion.

    Parametros:
    ==============

    p: Vector de poblacion/individuos.

    Retorna:
    ==============

    min: Aptitud minima.
    """
    min = p[0][1]

    for i in range(1, len(p)):

        if(min > p[i][1]):

            min = p[i][1]
    
    return min

def eliminarDuplicados(v):
    """
    Funcion para eliminar individuos duplicados de una poblacion.

    Parametros:
    ==============

    v: Vector de poblacion/individuos.

    Retorna:
    ==============

    n: Vector de poblacion sin individuos duplicados.
    """

    vistos = []
    n = []

    for i in v:
        if i[0] not in vistos:
            n.append(i)
            vistos.append(i[0])
    
    return n