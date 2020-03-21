#include <stdio.h>
#include <string.h>
#include <stdlib.h> // libreria para el uso de rand()  
#include <time.h>   // libreria para el uso de time()  
#include </usr/include/mpi/mpi.h>

int main(int argc, char *argv[]){

    int numeroProcesadores, idProceso, filas, contador;
    int hora = time(NULL); 
    long    *A, // Matriz a multiplicar
            *x, // Vector que vamos a multiplicar
            *y, // Vector donde almacenamos el resultado
            *miFila, // La fila que almacena localmente un proceso
            *miFila2;

    MPI_Init(&argc, &argv);  
    MPI_Comm_rank(MPI_COMM_WORLD, &idProceso);  
    MPI_Comm_size(MPI_COMM_WORLD, &numeroProcesadores); 

    // Semilla de rand();  
    srand(hora);

    // Cantidad de filas múltiplo de la cantidad de procesos.
    filas = rand() % (numeroProcesadores*2);
    while (filas < 2) {
        filas = rand() % numeroProcesadores;
    }
    

    // Reservamos tantas filas como procesos haya
    A =  (long*) malloc (filas*filas*sizeof(long)); 
    // for (int i=0; i<numeroProcesadores; i++) {
    //     A[i] = (long*) malloc (numeroProcesadores*sizeof(long));
    // }

    // El vector sera del mismo tamanio que el numero de procesadores
    x = (long*) malloc (filas*sizeof(long)); 

    if (idProceso == 0) {
        
        // Reservamos especio para el resultado
        y = (long*) malloc (filas*sizeof(long)); 

        // Carga de A y X
        printf("La matriz y el vector generados son: \n"); 

        // Carga de matriz A
        for (int i = 0; i < filas*filas; i++) {
            A[i] = rand() % 10;
        }

        // Carga vector x
        for (int i = 0; i < filas; i++) {
            x[i] = rand() % 10;
        }

        // Imprimo la matriz y el vector
        for (int i = 0; i < filas*filas; i++) {
            
            if (i%filas == 0) printf("["); 
            printf(" %ld ", A[i]);
            if ((i+1)%filas == 0) {
                printf("]\t  [ %ld ] \n", x[i/filas]);
            }

        }

    }
    
    // Reservamos espacio para la fila local de cada proceso
    miFila = (long*) malloc (filas*2*sizeof(long)); 
    miFila2 = (long*) malloc (2*sizeof(long)); 

    // Repartimos una fila por cada proceso, es posible hacer la reparticion de esta
    // manera ya que la matriz esta creada como un unico vector.
    MPI_Scatter(A, // Matriz que vamos a compartir
            filas*2, // Numero de columnas a compartir
            MPI_LONG, // Tipo de dato a enviar
            miFila, // Vector en el que almacenar los datos
            filas*2, // Numero de columnas a compartir
            MPI_LONG, // Tipo de dato a recibir
            0, // Proceso raiz que envia los datos
            MPI_COMM_WORLD); // Comunicador utilizado (En este caso, el global)

    // Compartimos el vector entre todas los procesos
    MPI_Bcast(x, // Dato a compartir
            filas, // Numero de elementos que se van a enviar y recibir
            MPI_LONG, // Tipo de dato que se compartira
            0, // Proceso raiz que envia los datos
            MPI_COMM_WORLD); // Comunicador utilizado (En este caso, el global)

    // Hacemos una barrera para asegurar que todas los procesos comiencen la ejecucion
    // a la vez, para tener mejor control del tiempo empleado
    MPI_Barrier(MPI_COMM_WORLD);

    long subFinal = 0;
    long subFinal2 = 0;
    for (int i = 0; i < filas; i++) {
        subFinal += miFila[i] * x[i];
    }
    for (int i = filas; i < filas*2; i++) {
        subFinal2 += miFila[i] * x[i-filas];
    }

    miFila2[0] = subFinal;
    miFila2[1] = subFinal2;

    // Otra barrera para asegurar que todas ejecuten el siguiente trozo de codigo lo
    // mas proximamente posible
    MPI_Barrier(MPI_COMM_WORLD);

    // Recogemos los datos de la multiplicacion, por cada proceso sera un escalar
    // y se recoge en un vector, Gather se asegura de que la recoleccion se haga
    // en el mismo orden en el que se hace el Scatter, con lo que cada escalar
    // acaba en su posicion correspondiente del vector.
    MPI_Gather(miFila2, // Dato que envia cada proceso
            2, // Numero de elementos que se envian
            MPI_LONG, // Tipo del dato que se envia
            y, // Vector en el que se recolectan los datos
            2, // Numero de datos que se esperan recibir por cada proceso
            MPI_LONG, // Tipo del dato que se recibira
            0, // proceso que va a recibir los datos
            MPI_COMM_WORLD); // Canal de comunicacion (Comunicador Global)

    MPI_Finalize(); 

    if (idProceso == 0) {
        
        printf("El resultado es: \n");
        for (int i = 0; i < filas; i++) {
            printf("[%ld] \n", y[i]);
        }

    }
    
    
    return 0;
}

