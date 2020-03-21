// El procesos con pid = 0 recibe mensajes de los demas procesos y los muestra 
// por pantalla. Igual ap ejercicio 1_b, solo que en este recibe los mensajes
// en orden.

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

    if (mytid == 0){
        printf("Hola, soy el proceso 0 (hay “%d” procesos) y recibo:\n", nproc-1);
        for(int i=1;i<nproc;i++){
            MPI_Recv(message, 18, MPI_CHAR, i, 99, MPI_COMM_WORLD, &status);
            printf("%s\n", message);
        }
    }
    else{
        sprintf(message,"Soy el proceso: %d",mytid);
        MPI_Send(message, strlen(message)+1, MPI_CHAR, 0, 99, MPI_COMM_WORLD);
    }

    MPI_Finalize();
}