#include <stdio.h>
#include <string.h>
#include </usr/include/mpi/mpi.h>

int main(int argc, char **argv){

    int prod, num_procs, my_rank, num, mensaje, res, op;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    num = my_rank + 1;
    MPI_Send(&num, 1, MPI_INT, 0, 99, MPI_COMM_WORLD);

    if (my_rank == 0) {

        printf("Hola soy el proceso %d, ingresa una operacion (al proceso n se le asigna el numero n+1) \n", my_rank);
        printf("1 = + \n");
        printf("2 = * \n");
        printf("3 = MAX \n");
        printf("4 = MIN \n");
        scanf("%d", &op);

        for(int i=0;i<num_procs;i++){

            MPI_Recv(&mensaje, 1, MPI_INT, i, 99, MPI_COMM_WORLD, &status);
            //printf("soy el proceso %d y mi numero es: %d \n", i, mensaje);

            switch (op){
            case 1:
                if (i == 0) res = 1;
                else res += mensaje;
                break;
            case 2:
                if (i == 0) res = 1;
                else res *= mensaje;
                break;
            case 3:
                if (i == 0) res = mensaje;
                else{
                    if (res < mensaje) res = mensaje;
                }
                break;
            case 4:
                if (i == 0) res = mensaje;
                else{
                    if (res > mensaje) res = mensaje;
                }
                break;
            default:
                break;
            }

        }
        
        printf("Hola, soy el proceso %d y la operacion devuelve: %d\n", my_rank, res);
    }

    MPI_Finalize();

}