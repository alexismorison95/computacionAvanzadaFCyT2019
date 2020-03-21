#include<stdio.h>
#include</usr/include/mpi/mpi.h>

int main(int argc, char **argv){
    int idProceso;
    MPI_Init(&argc, &argv); //acá se inicializa el mpi
    MPI_Comm_rank(MPI_COMM_WORLD, &idProceso); //
    printf("Hello World from process %d\n",idProceso);
    MPI_Finalize();
}



