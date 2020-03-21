#include <stdio.h>
#include <string.h>
#include </usr/include/mpi/mpi.h>

int main(int argc, char *argv[]){  
    MPI_Status status;  
    int num, rank, size, tag, next, from; 
    char message;
    
    MPI_Init(&argc, &argv);  
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  
    MPI_Comm_size(MPI_COMM_WORLD, &size);  

    message = 'A';  
    next = (rank + 1) % size;  
    from = (rank + size - 1) % size;  

    if (rank == 0) {  
        
        printf("Introduce el numero de vueltas al anillo: \n");    
        scanf("%d", &num);   
        
        printf("El proceso %d envia el %d al proceso %d\n", rank, num, next);    
        MPI_Send(&num, 1, MPI_INT, next, tag, MPI_COMM_WORLD);   

    }  

    /* Los procesos "pasan" el numero de vueltas que faltan.
  Cuando llega al proceso 0, se descuenta una vuelta.
  Cuando un proceso recibe un 0, lo pasa y termina. */

    do {    

        MPI_Recv(&num, 1, MPI_INT, from, tag, MPI_COMM_WORLD, &status);  
        printf("Proceso %d ha recibido %d\n", rank, num);  
 
        if (rank == 0) {      
            --num;      
            printf("Proceso 0 descuenta una vuelta, vuelta: %d\n", num);    
        }    

        printf("El proceso %d envia %d al proceso %d\n", rank, num, next);   
        MPI_Send(&num, 1, MPI_INT, next, tag, MPI_COMM_WORLD);  

    } while (num > 0); 
    
     /* El proceso 0 debe esperar el ultimo envio del ultimo proceso antes de terminar */
    if (rank == 0) {
        MPI_Recv(&num, 1, MPI_INT, from, tag, MPI_COMM_WORLD, &status);  
    }

    MPI_Finalize(); 
    
    return 0;
}