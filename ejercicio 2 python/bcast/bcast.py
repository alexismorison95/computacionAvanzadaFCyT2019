from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()

# El proceso 0 genera los datos
if(idProceso == 0):

    datos = np.random.randint(0, 10, size=(1, cantidadProcesos*cantidadProcesos))
    print("Soy el proceso 0 y genere los datos:", datos)
    print()

else:
    # Los demas procesos tambien tienen que tener definida la variable
    datos = None

# Comunicacion colectiva
datos = comm.bcast(datos, root=0)

# Cada proceso imprime los datos recibidos
print("Soy el proceso", idProceso, "y recibi:", datos)