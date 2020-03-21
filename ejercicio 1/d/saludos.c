// idem a los anteriores solo que esta vez el proceso encargado de recibir los
// mensajes es el proceso con pid = 1.

#include <stdio.h>
#include </usr/include/mpi/mpi.h>
#include <string.h>

int main(int argc, char **argv){

    int nproc, mytid;
    char message[20]; 
    MPI_Status status;
    MPI_Init(&argc, &argv); //acá se inicializa el mpi
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    MPI_Comm_rank(MPI_COMM_WORLD, &mytid);

    if (mytid == 1){
        printf("Hola, soy el proceso %d (hay “%d” procesos) y recibo:\n", mytid, nproc-1);
        for(int i=0;i<nproc;i++){
            if (i != 1){
                MPI_Recv(message, 18, MPI_CHAR, i, 99, MPI_COMM_WORLD, &status);
                printf("%s\n", message);
            }
        }
    }
    else{
        sprintf(message,"Soy el proceso: %d",mytid);
        MPI_Send(message, strlen(message)+1, MPI_CHAR, 1, 99, MPI_COMM_WORLD);
    }

    MPI_Finalize();
}