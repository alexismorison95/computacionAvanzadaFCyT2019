from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()

# Creo un numero random
dato = random.randint(0, 10)
print("Soy el proceso", idProceso, "y mi numero es", dato)

# Comunicacion colectiva
fila = comm.gather(dato, root=0)

if(idProceso == 0):
    # El proceso 0 es el que recibe los datos
    print("Soy el proceso 0 y mis datos son", fila)