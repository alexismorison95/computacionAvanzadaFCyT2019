// alltoall implementado con send y recv, auqnue de momento solo funciona para 3
// procesos solamente.

#include <stdio.h>
#include <string.h>
#include <stdlib.h> // libreria para el uso de rand()  
#include <time.h>   // libreria para el uso de time()  
#include </usr/include/mpi/mpi.h>

int main(int argc, char **argv){

    int numeroProcesadores, idProceso;
    char message;
    long *A, *fila1, *fila2;
    MPI_Status status;
    int hora = time(NULL); 
    
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &numeroProcesadores);
    MPI_Comm_rank(MPI_COMM_WORLD, &idProceso);

    // Semilla de rand();  
    srand(hora);

    A = (long*) malloc (numeroProcesadores*numeroProcesadores*sizeof(long));

    // El proceso 0 carga la matriz
    if (idProceso == 0) {

        printf("Proceso 0 crea la matriz: \n");
        
        // Carga de matriz A
        for (int i = 0; i < numeroProcesadores*numeroProcesadores; i++) {
            A[i] = rand() % 10;
        }

        // Imprimo la matriz y el vector
        for (int i = 0; i < numeroProcesadores*numeroProcesadores; i++) {
            
            if (i%numeroProcesadores == 0) printf("["); 
            printf(" %ld ", A[i]);
            if ((i+1)%numeroProcesadores == 0) {
                printf("]\n");
            }

        }

        // envio a cada proceso su fila
        for (int i = 0; i < numeroProcesadores; i++) {

            MPI_Send(&A[i*numeroProcesadores], numeroProcesadores, MPI_LONG, i, 99, MPI_COMM_WORLD);
        
        }

    }

    // cada proceso recibe la fila que tiene que envio el proceso 0
    fila1 = (long*) malloc (numeroProcesadores*sizeof(long));

    MPI_Recv(fila1, numeroProcesadores, MPI_LONG, 0, 99, MPI_COMM_WORLD, &status);


    // envio elemento correspondiente a cada proceso para trasponer
    for (int i = 0; i < numeroProcesadores; i++) {

        MPI_Send(&fila1[i], 1, MPI_LONG, i, 99, MPI_COMM_WORLD);

    }

    // recibo los elementos traspuestos
    fila2 = (long*) malloc (numeroProcesadores*sizeof(long));

    for (int i = 0; i < numeroProcesadores; i++) {

        MPI_Recv(fila2+i, 1, MPI_LONG, i, 99, MPI_COMM_WORLD, &status);

    }

    // imprimo la fila de cada proceso
    printf("Proceso %d recibio fila traspuesta:   ", idProceso);

    for (int i = 0; i < numeroProcesadores; i++){
        
        printf(" %ld ", fila2[i]);

    }
    printf("\n");

    MPI_Finalize();

    return 0;
}