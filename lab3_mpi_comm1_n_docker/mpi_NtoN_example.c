#include <mpi.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv) {
  MPI_Init(&argc, &argv);

  int world_size, world_rank;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);  // Get number of processes
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);  // Get rank of process

  int gathered_values[world_size];

  MPI_Allgather(&world_rank, 1, MPI_INT, gathered_values, 1, MPI_INT,
                MPI_COMM_WORLD);

  printf("(ALLGATHER) Process %d -> Send value %d | gathered array: ",
         world_rank, world_rank);
  for (int i = 0; i < world_size; i++) {
    printf("%d ", gathered_values[i]);
  }
  printf("\n");

  sleep(2);

  int reduced_value[world_size];
  for (int i = 0; i < world_size; i++) {
    reduced_value[i] = 0;
  }

  // Perform the reduction operation (sum) with root process being rank 0
  MPI_Reduce(&gathered_values, &reduced_value, world_size, MPI_INT, MPI_SUM, 0,
             MPI_COMM_WORLD);

  printf("(REDUCE) Process %d: The sum of all process values is: ", world_rank);
  for (int i = 0; i < world_size; i++) {
    printf("%d ", reduced_value[i]);
  }
  printf("\n");

  sleep(2);

  MPI_Allreduce(&gathered_values, &reduced_value, world_size, MPI_INT, MPI_SUM,
                MPI_COMM_WORLD);

  printf("(ALLREDUCE) Process %d: The sum of all process values is: ",
         world_rank);
  for (int i = 0; i < world_size; i++) {
    printf("%d ", reduced_value[i]);
  }
  printf("\n");

  MPI_Finalize();
  return 0;
}
