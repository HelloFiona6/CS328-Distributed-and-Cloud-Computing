#include <mpi.h>
#include <stdio.h>
#include <unistd.h> // lib for sleep

#define ROOT 0

int main(int argc, char **argv)
{
    MPI_Init(NULL, NULL);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // ensure the size
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    if (world_size != 4)
    {
        fprintf(stderr, "World size must be four for %s\n", argv[0]);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int arr_size = 2;
    int gatherbuf[world_size];
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
    else
    {
        ////////////////////// receive bcast ////////////////////////////////////////////
        int rcv_data[arr_size]; // store received data
        // receive broadcasted data
        MPI_Bcast(&rcv_data, arr_size, MPI_INT, 0, MPI_COMM_WORLD);

        int final_data;
        char operation[2];

        if (world_rank == 0)
        {
            final_data = rcv_data[0] + rcv_data[1];
            sprintf(operation, "+");
        }
        else if (world_rank == 1)
        {
            final_data = rcv_data[0] - rcv_data[1];
            sprintf(operation, "-");
        }
        else if (world_rank == 2)
        {
            final_data = rcv_data[0] * rcv_data[1];
            sprintf(operation, "*");
        }
        else if (world_rank == 3)
        {
            final_data = rcv_data[0] / rcv_data[1];
            sprintf(operation, "/");
        }

        // All processes should now have the same data
        printf("Process %d data after %s operation: ", world_rank, operation);

        printf("%d\n", final_data);
        ////////////////////////// gather ////////////////////////////////////////////////////

        MPI_Gather(&final_data, 1, MPI_INT, &gatherbuf, 1,
                   MPI_INT, ROOT, MPI_COMM_WORLD);
    }

    // root prints gather list
    if (world_rank == ROOT)
    {
        sleep(1);
        printf("Root (Process 0) gathered the following list from the workers: ");
        for (int i = 0; i < world_size; i++)
        {
            printf("%d ", gatherbuf[i]);
        }
        printf("\n");
    }

    // Finalize the MPI environment. No more MPI calls can be made after this
    MPI_Finalize();
}
