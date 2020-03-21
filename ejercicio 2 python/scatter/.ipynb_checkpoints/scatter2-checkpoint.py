from mpi4py import MPI
import numpy as np
import random

comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()

# Tamanio del arreglo original (Debe ser divicible por la cantidad de procesos)
n = 4 
# Tamanio del sub vector de cada proceso
miN = n // cantidadProcesos

# Inicializo los arreglos vacios
datos = np.empty(n, dtype=np.int)       # SendBuff
misDatos = np.empty(miN, dtype=np.int)  # RecvBuff

if(idProceso == 0):
    # El proceso 0 se encarga de cargar el arreglo random
    datos = np.random.randint(0, 10, size=(1, n))

    print("Soy el proceso 0 y los datos son", datos)
    print()

# Comunicacion colectiva
comm.Scatter([datos, MPI.INT], [misDatos, MPI.INT])

print("Soy el proceso", idProceso, "y mis datos son", misDatos)