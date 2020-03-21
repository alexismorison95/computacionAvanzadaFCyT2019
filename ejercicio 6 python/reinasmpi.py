# Imports
from datetime import datetime
import random
from mpi4py import MPI

from funciones import cruzaYMutacion, individuoRandom, dividirPoblacion, obtenerAptitud, unirPoblacion, imprimirTablero, aptitud, aptitudMinima, aptitudPromedio, reinas, porcentajeMutacion, porcentajeCruza, eliminarDuplicados


# PARAMETROS
cantGeneraciones = 250        
generacionInicial = 400  
comunicoCada = 1  # Parametro que indica cada cuantas generaciones se comunican los procesos

# Para 8 reinas: cantGeneraciones = 25, generacionInicial = 80 | OPTIMO
# Para 16 reinas: cantGeneraciones = 250, generacionInicial = 400 | OPTIMO

# INICIO DEL PROGRAMA
# mpiexec -n 4 python reinasmpi.py


comm = MPI.COMM_WORLD
idProceso = comm.Get_rank()
cantidadProcesos = comm.Get_size()

comm.Barrier()

# Creo el vector poblacion (general)
poblacion = []
# Vector subPoblacion para cada proceso
subPoblacion = []

# El porceso 0 se encarga de crear la poblacion inicial
if (idProceso == 0):

    # armo la poblacion inicial randomicamente
    for i in range(generacionInicial): 

        # El modelo del individuo es una tupla (genoma, fitness)
        individuo = []
        individuo.append(individuoRandom())   # cargo el genoma del individuo
        individuo.append(aptitud(individuo[0])) # cargo la aptitud del individuo      

        poblacion.append(individuo)             # cargo el individuo a la poblacion

    # Parto la poblacion en sub poblaciones, para poder mandar las porciones a traves del scatter
    poblacion = dividirPoblacion(poblacion, generacionInicial//cantidadProcesos)

    instanteInicial = datetime.now() # inicio un cronometro


# Ciclo de generaciones para cada proceso
for i in range(cantGeneraciones):

    # Envio cada porcion de poblacion al proceso correspondiente
    miPoblacion = comm.scatter(sendobj=poblacion, root=0)

    # Cruzas y mutaciones
    miPoblacion = cruzaYMutacion(miPoblacion)

    # Codigo para descartar los individuos menos aptos de cada proceso
    # Esta linea se ejecuta cuando los procesos no se comunican en cada generacion.
    # En la practica se nota una perdida de eficacia.
    # miPoblacion.sort(key=obtenerAptitud)
    # miPoblacion = miPoblacion[:generacionInicial]

    # Aca manejamos cada cuantas generaciones queremos que se comuniquen los procesos
    # Actualmente se comunican en cada generacion
    if (i%comunicoCada == 0):

        # Gather para devolver toda la poblacion al proceso 0
        poblacion = comm.gather(sendobj=miPoblacion, root=0)

        if (idProceso == 0):

            # SELECCION
            # Ordenamos la poblacion por fitness y recortamos la poblacion a poblacionInicial
            poblacion = unirPoblacion(poblacion)
            poblacion.sort(key=obtenerAptitud)
            poblacion = poblacion[:generacionInicial]

            # Desordeno la poblacion para que los mejores individuos no queden siempre para el proceso 0
            random.shuffle(poblacion)

            # Parto la poblacion en sub poblaciones, para poder mandar las porciones a traves del scatter
            poblacion = dividirPoblacion(poblacion, generacionInicial//cantidadProcesos)
    
    if (cantGeneraciones%(i+1) == 0):
        # Imprimo informacion util cada cierta cantidad de generaciones para cada proceso
        print(
            "Proceso " + str(idProceso) + 
            ".  Generacion " + str(i) + 
            ",  Aptitud minima = " + str(aptitudMinima(miPoblacion)) + 
            ",  Aptitud promedio = " + str(round(aptitudPromedio(miPoblacion))) + 
            ",  Tamanio de poblacion = " + str(len(miPoblacion))
        )

print()
comm.Barrier()

# Terminan las generaciones
if (idProceso == 0):

    instanteFinal = datetime.now() # finalizo el cronometro
    tiempo = instanteFinal - instanteInicial # Devuelve un objeto timedelta

    # Vuelvo a unir la poblacion en un solo vector
    poblacion = unirPoblacion(poblacion)

    # Elimino individuos duplicados
    poblacion = eliminarDuplicados(poblacion) 

    # Ordeno y recorto la poblacion para quedarme con los 8 mejores
    poblacion.sort(key=obtenerAptitud)
    poblacion = poblacion[:reinas]
    
    print(str(reinas) + " mejores individuos en " + str(cantGeneraciones) + " generaciones, obtenidos en " + str(tiempo) + " segundos")
    print()

    # Imprimo los mejores resultados
    for i in range(len(poblacion)):

        print("Individuo", poblacion[i][0], "- Ataques:", poblacion[i][1])
        #imprimirTablero(poblacion[i])

