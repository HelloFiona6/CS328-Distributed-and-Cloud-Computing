#include <mpi.h>
#include <stdio.h>

int main(int argc){
int a;
return 0;
}
/*
为什么c语言吧bcast_data写在if内外会导致world_rank==0收到的消息不一样
   int arr_size = 2;
int bcast_data[arr_size];


    /////////////////////// bcast /////////////////////////////////////////////////////
    if (world_rank == 0)
    {
        int bcast_data[arr_size];
        bcast_data[0] = 6; // init
        bcast_data[1] = 2;

        printf("Process %d broadcasting data: ", world_rank);
        for (int i = 0; i < arr_size; i++)
        {
            printf("|%d: %d|\t", i, bcast_data[i]);
        }
        printf("\n");
        fflush(stdout);

        // Broadcast the data from process 0 to all other processes
        MPI_Bcast(&bcast_data, arr_size, MPI_INT, 0, MPI_COMM_WORLD);
    }

    ////////////////////// receive bcast ////////////////////////////////////////////
    int rcv_data[arr_size]; // store received data
    // receive broadcasted data
    MPI_Bcast(&rcv_data, arr_size, MPI_INT, 0, MPI_COMM_WORLD);

*/