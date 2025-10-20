#include <mpi.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
  MPI_Init(&argc, &argv);

  int rank, size;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  int sendbuf[size];
  int recvbuf[size];  // Buffer to receive data from other processes

  // Initialize the send buffer with unique values
  for (int i = 0; i < size; i++) {
    // e.g., Process 0 will have {0, 1, 2, 3},
    // Process 1 will have {10, 11, 12, 13}
    sendbuf[i] = rank * 10 + i;
  }

  // Perform the all-to-all communication
  MPI_Alltoall(sendbuf, 1, MPI_INT, recvbuf, 1, MPI_INT, MPI_COMM_WORLD);

  // Output the result
  printf("Process %d received: ", rank);
  for (int i = 0; i < size; i++) {
    printf("%d ", recvbuf[i]);
  }
  printf("\n");

  MPI_Finalize();
  return 0;
}
