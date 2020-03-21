// idem a los anteriores pero los mensajes son no bloqueantes

#include <stdio.h>
#include <string.h>
#include </usr/include/mpi/mpi.h>

int main(int argc, char **argv){

    int my_rank, nproc, n, message, recibido;
    //char n, message[20];
    MPI_Status status;
    MPI_Request request;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    if (my_rank == 0) {

        printf("Hola soy el proceso %d, ingresa un número: \n", my_rank);
        scanf("%d", &n); //lo guarda en n

        for(int x=0;x<nproc;x++){

            MPI_Isend(&n, 1, MPI_INT, x, 99, MPI_COMM_WORLD, &request);

            MPI_Wait(&request, &status);

        }

    }

    MPI_Irecv(&message, 1, MPI_INT, 0, 99, MPI_COMM_WORLD, &request);

    MPI_Wait(&request, &status);

    
    printf("Hola, soy el proceso %d y el número es el %d \n", my_rank, message);

    MPI_Finalize();
    
}