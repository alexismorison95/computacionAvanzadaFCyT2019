from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()

# Creo un vector con la logitud de la cantidad de procesos
x = np.arange(cantidadProcesos, dtype=np.int) + idProceso 
print("Soy el Proceso", idProceso, "- mi vector es", x)

# Creo la matriz donde voy a almacenar el resultado del all gather
y = np.zeros((cantidadProcesos, len(x)), dtype=np.int)

# Comunicacion colectiva
comm.Allgather([x, MPI.INT], [y, MPI.INT])

print("Soy el proceso", idProceso, "y recibo:")
print(y)