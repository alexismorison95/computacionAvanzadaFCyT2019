// Lo que hace es que todos los procesos envian a todos los procesos su pid
// cada procesos cuando recibe los pid los va sumando en una variable y luego lo
// muestra por pantalla.

#include <stdio.h>
#include <string.h>
#include </usr/include/mpi/mpi.h>

int main(int argc, char **argv){

    int sum, num_procs, num, mensaje, my_rank;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    num = my_rank;

    for (int i = 0; i < num_procs; i++) {
        MPI_Send(&num, 1, MPI_INT, i, 99, MPI_COMM_WORLD);
    }
    
    sum = 0;

    for(int i = 0; i < num_procs; i++) {

        MPI_Recv(&mensaje, 1, MPI_INT, MPI_ANY_SOURCE, 99, MPI_COMM_WORLD, &status);

        sum += mensaje;

    }
    
    printf("Hola, soy el proceso %d y recibi %d \n", my_rank, sum);


    MPI_Finalize();

}