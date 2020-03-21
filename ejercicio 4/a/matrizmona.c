#include <stdio.h>
#include <string.h>
#include <stdlib.h> // libreria para el uso de rand()  
#include <time.h>   // libreria para el uso de time()  
#include </usr/include/mpi/mpi.h>

int main(int argc, char *argv[]){

    int numeroProcesadores, idProceso;
    int hora = time(NULL); 
    long    **A, // Matriz a multiplicar
            *x, // Vector que vamos a multiplicar
            *y, // Vector donde almacenamos el resultado
            *miFila; // La fila que almacena localmente un proceso

    MPI_Init(&argc, &argv);  
    MPI_Comm_rank(MPI_COMM_WORLD, &idProceso);  
    MPI_Comm_size(MPI_COMM_WORLD, &numeroProcesadores); 

    // Semilla de rand();  
    srand(hora); 

    // Reservamos tantas filas como procesos haya
    A =  (long**) malloc (numeroProcesadores*sizeof(long)); 
    // for (int i=0; i<numeroProcesadores; i++) {
    //     A[i] = (long*) malloc (numeroProcesadores*sizeof(long));
    // }

    // El vector sera del mismo tamanio que el numero de procesadores
    x = (long*) malloc (numeroProcesadores*sizeof(long)); 

    if (idProceso == 0) {

        A[0] = (long*) malloc (numeroProcesadores*numeroProcesadores*sizeof(long));
        for (unsigned int i = 1; i < numeroProcesadores; i++) {
            A[i] = A[i - 1] + numeroProcesadores;
        } 
        
        // Reservamos especio para el resultado
        y = (long*) malloc (numeroProcesadores*sizeof(long)); 


        for ( int i = 0; i < numeroProcesadores; i++)
        {
            /* code */
        }
        

        // Carga de A y X
        printf("La matriz y el vector generados son: \n"); 
        for (int i = 0; i < numeroProcesadores; i++) {
            for (int j = 0; j < numeroProcesadores; j++) {
                if (j == 0) printf("["); 
                A[i][j] = rand()%10;
                printf("%ld", A[i][j]);
                if (j == numeroProcesadores - 1) printf("]");
                else printf("  ");
            }
            x[i] = rand() % 10;
            printf("\t  [%ld] \n", x[i]);
        }
        printf("\n");
        
    }
    
    // Reservamos espacio para la fila local de cada proceso
    miFila = (long*) malloc (numeroProcesadores*sizeof(long)); 

    // Repartimos una fila por cada proceso, es posible hacer la reparticion de esta
    // manera ya que la matriz esta creada como un unico vector.
    
    
    
    MPI_Scatter(A[0], // Matriz que vamos a compartir
            numeroProcesadores, // Numero de columnas a compartir
            MPI_LONG, // Tipo de dato a enviar
            miFila, // Vector en el que almacenar los datos
            numeroProcesadores, // Numero de columnas a compartir
            MPI_LONG, // Tipo de dato a recibir
            0, // Proceso raiz que envia los datos
            MPI_COMM_WORLD); // Comunicador utilizado (En este caso, el global)

    // Compartimos el vector entre todas los procesos
    MPI_Bcast(x, // Dato a compartir
            numeroProcesadores, // Numero de elementos que se van a enviar y recibir
            MPI_LONG, // Tipo de dato que se compartira
            0, // Proceso raiz que envia los datos
            MPI_COMM_WORLD); // Comunicador utilizado (En este caso, el global)

    // Hacemos una barrera para asegurar que todas los procesos comiencen la ejecucion
    // a la vez, para tener mejor control del tiempo empleado
    MPI_Barrier(MPI_COMM_WORLD);

    long subFinal = 0;
    for (unsigned int i = 0; i < numeroProcesadores; i++) {
        subFinal += miFila[i] * x[i];
    }

    // Otra barrera para asegurar que todas ejecuten el siguiente trozo de codigo lo
    // mas proximamente posible
    MPI_Barrier(MPI_COMM_WORLD);

    // Recogemos los datos de la multiplicacion, por cada proceso sera un escalar
    // y se recoge en un vector, Gather se asegura de que la recoleccion se haga
    // en el mismo orden en el que se hace el Scatter, con lo que cada escalar
    // acaba en su posicion correspondiente del vector.
    MPI_Gather(&subFinal, // Dato que envia cada proceso
            1, // Numero de elementos que se envian
            MPI_LONG, // Tipo del dato que se envia
            y, // Vector en el que se recolectan los datos
            1, // Numero de datos que se esperan recibir por cada proceso
            MPI_LONG, // Tipo del dato que se recibira
            0, // proceso que va a recibir los datos
            MPI_COMM_WORLD); // Canal de comunicacion (Comunicador Global)

    MPI_Finalize(); 

    if (idProceso == 0) {
        
        printf("El resultado es: \n");
        for (int i = 0; i < numeroProcesadores; i++) {
            printf("[%ld] \n", y[i]);
        }

    }
    
    
    return 0;
}

