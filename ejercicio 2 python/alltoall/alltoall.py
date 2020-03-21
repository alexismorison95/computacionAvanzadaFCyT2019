from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()


# Cargo una fila random
m = np.random.randint(0, 10, size=(cantidadProcesos, 1), dtype=np.int)

# Barrera por las dudas
comm.barrier()

# Imprimo mi fila
aux = ""
for i in range(cantidadProcesos):
    aux += str(m[i])

print("Soy el proceso", idProceso, "y GENERE la fila:", aux)

# Vector donde se almacena la fila luego del alltoall
r = np.zeros((cantidadProcesos, 1), dtype=np.int)

# Comunicacion colectiva
comm.Alltoall(m, r)

# Imprimo el resultado
aux = ""
for i in range(cantidadProcesos):
    aux += str(r[i])

print("Soy el proceso", idProceso, "y recibi la fila:               ", aux)