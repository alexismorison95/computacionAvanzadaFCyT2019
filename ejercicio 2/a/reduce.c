// Reduce implementado con send y recv, todos los procesos mandan su pid + 1
// y el proceso 0 hace la multiplicacion simulando el calculo del factorial.

#include <stdio.h>
#include <string.h>
#include </usr/include/mpi/mpi.h>

int main(int argc, char **argv){

    int prod, num_procs, my_rank, num, mensaje;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    num = my_rank + 1;
    printf("soy el proceso %d y el mensaje es: %d \n", my_rank, num);
    MPI_Send(&num, 1, MPI_INT, 0, 99, MPI_COMM_WORLD);
    

    if (my_rank == 0) {

        prod = 1;

        for(int i=0;i<num_procs;i++){

            MPI_Recv(&mensaje, 1, MPI_INT, MPI_ANY_SOURCE, 99, MPI_COMM_WORLD, &status);
            
            prod = mensaje * prod;
        }
        
        printf("Hola, soy el proceso %d y el factorial de %d es %d\n", my_rank, num_procs, prod);
    }

    MPI_Finalize();

}