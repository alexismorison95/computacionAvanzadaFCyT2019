# Imports
import numpy as np
from mpi4py import MPI

from funciones import mostrarTablero, aplicarReglas, cargarMatrizRandom, cortarMatriz, unirMatriz, concatenarMatrices, cortarExcedente


# Constantes
cantGeneraciones = 10
n = 20 # dimension de matriz

# INICIO DEL PROGRAMA
# mpiexec -n 4 python vidaMPI.py

comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()

comm.Barrier()

# Creo la matriz vacia
matriz = np.zeros((n, n), np.int)

if(idProceso == 0):

    # El proceso 0 carga la matriz
    matriz = cargarMatrizRandom(n)

    mostrarTablero((matriz, 0))


# Ciclo de generaciones/evoluciones
for i in range(cantGeneraciones):

    if(idProceso == 0):

        # El proceso 0 se encarga de cortar la matriz para poder hacer el scatter
        matriz = cortarMatriz(matriz, cantidadProcesos)

    # Comunicacion colectiva Scatter
    miSubMatriz = comm.scatter(sendobj=matriz, root=0)

    # Cada proceso aplica las reglas
    miSubMatriz = aplicarReglas(miSubMatriz)

    # Cada proceso corta las filas de referencia de cada matriz
    miSubMatriz = cortarExcedente(miSubMatriz, idProceso, cantidadProcesos)

    # Comunicacion colectiva Gather
    matriz = comm.gather(sendobj=miSubMatriz, root=0)

    # El proceso 0 se encarga de volver a armar la matriz y mostrarla
    if (idProceso == 0):

        # Sacamos este metodo ya que encontramos una forma mas facil
        #init = unirMatriz(init, cantidadProcesos) 

        # Concateno las submatrices para poder mostrar la nueva generacion
        matriz = concatenarMatrices(matriz)

        # Muestro el tablero
        mostrarTablero((matriz, i+1))