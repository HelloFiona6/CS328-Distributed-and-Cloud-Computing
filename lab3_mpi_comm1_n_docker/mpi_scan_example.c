#include <mpi.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv) {
  MPI_Init(&argc, &argv);

  int world_size, world_rank;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);  // Get number of processes
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);  // Get rank of process

  int scanned_value;

  MPI_Scan(&world_rank, &scanned_value, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);

  printf("Process %d -> scaned value: %d \n", world_rank, scanned_value);

  MPI_Finalize();
  return 0;
}
