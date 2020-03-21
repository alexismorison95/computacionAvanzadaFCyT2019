from mpi4py import MPI
import numpy as np
import random

comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()

datos = None
# El proceso 0 crea un vector con el tamanio de la cantidad de procesos
if(idProceso == 0):

    datos = []
    for i in range(cantidadProcesos):
        datos.append(random.randint(0, 100))
    
    print("Soy el proceso 0 y los datos son:", datos)
    print()

# Comunicacion colectiva
datos = comm.scatter(datos, root=0)
# Con este scatter a cada proceso se le puede dar un solo elemento

print("Soy el proceso", idProceso, " y mi dato es", datos)