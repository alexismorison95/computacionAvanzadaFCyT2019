// scatter implementado con send y recv, lo que hace es que el proceso 0 arma un vector
// con tantos numeros como procesos y envia a cada proceso el numero + 1.
// ejemplo: al proceso 0 envia el 1
//          al proceso 1 el 2 y asi sucesivamente.

#include <stdio.h>
#include <string.h>
#include </usr/include/mpi/mpi.h>

int main(int argc, char **argv){

    int my_rank, nproc, message;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    int vector[nproc];

    if (my_rank == 0) {

        printf("Hola soy el proceso %d y voy a mandar al proceso n, el n+1 del arreglo ", my_rank);
        printf("[ ");

        for(int x=0;x<nproc;x++) {

            vector[x] = x+1;
            printf("%d ", x+1);

        }

        printf("] \n");

        for(int x=0;x<nproc;x++) {

            MPI_Send(&vector[x], 1, MPI_INT, x, 99, MPI_COMM_WORLD);

        }

    }

    MPI_Recv(&message, 1, MPI_INT, 0, 99, MPI_COMM_WORLD, &status);
    printf("Hola, soy el proceso %d y el número recibido es: %d \n", my_rank, message);

    MPI_Finalize();
    
}