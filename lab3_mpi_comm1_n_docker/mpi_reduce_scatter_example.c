#include <mpi.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
  MPI_Init(&argc, &argv);

  int rank, size;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  int sendbuf[size];  // Data to be scattered and later reduced
  int recvbuf;        // Buffer to store the scattered result

  // Initialize the send buffer with unique values per process
  for (int i = 0; i < size; i++) {
    // e.g., Process 0 will have {0, 1, 2, 3},
    // Process 1 will have {10, 11, 12, 13}
    sendbuf[i] = rank * 10 + i;
  }

  // how many values each processes will receive (it needs to be an array even
  // if all processes receive the same number of data)
  int receive_counts[size];
  for (int i = 0; i < size; i++) {
    receive_counts[i] = 1;
  }

  // Perform the reduce-scatter operation (using MPI_SUM)
  MPI_Reduce_scatter(sendbuf, &recvbuf, receive_counts, MPI_INT, MPI_SUM,
                     MPI_COMM_WORLD);

  // Output the result
  printf("Process %d received: %d \n", rank, recvbuf);

  MPI_Finalize();
  return 0;
}
