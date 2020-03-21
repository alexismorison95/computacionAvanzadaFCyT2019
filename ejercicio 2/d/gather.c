// gather implementado con send y recv, lo que hace es que cada proceso envia un numero
// y el proceso 0 los recibe y los guarda en un vector.

#include <stdio.h>
#include <string.h>
#include </usr/include/mpi/mpi.h>

int main(int argc, char **argv){

    int prod, num_procs, my_rank, num, mensaje;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    int rec[num_procs];

    num = my_rank + 1;
    MPI_Send(&num, 1, MPI_INT, 0, 99, MPI_COMM_WORLD);

    if (my_rank == 0) {

        for(int i=0;i<num_procs;i++){

            MPI_Recv(&mensaje, 1, MPI_INT, MPI_ANY_SOURCE, 99, MPI_COMM_WORLD, &status);
            printf("soy el proceso %d y el mensaje es: %d \n", i, mensaje);
            
            rec[i] = mensaje;
        }
        
        printf("Hola, soy el proceso %d y recibi: [", my_rank);

        for (int i = 0; i < num_procs; i++) {
            printf(" %d", rec[i]);
        }
        printf(" ]\n");
        
    }

    MPI_Finalize();

}