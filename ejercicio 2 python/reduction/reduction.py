from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()

# Creo un numero random
dato = random.randint(0, 100)
print("Soy el proceso", idProceso, "y mi numero es", dato)

# Comunicacion colectiva
res = comm.reduce(dato, op=MPI.MAX, root=0)
# MPI_MAX 	Máximo entre los elementos
# MPI_MIN 	Mínimo entre los elementos
# MPI_SUM 	Suma
# MPI_PROD 	Producto
# MPI_LAND 	AND lógico (devuelve 1 o 0, verdadero o falso)
# MPI_BAND 	AND a nivel de bits
# MPI_LOR 	OR lógico
# MPI_BOR 	OR a nivel de bits
# MPI_LXOR 	XOR lógico
# MPI_BXOR 	XOR a nivel de bits
# MPI_MAXLOC 	Valor máximo entre los elementos y el rango del proceso que lo tenía
# MPI_MINLOC 	Valor mínimo entre los elementos y el rango del proceso que lo tenía

if(idProceso == 0):
    # El proceso 0 es el que recibe el resultado de la operacion
    print("Soy el proceso 0 y el resultado de la operacion es", res)