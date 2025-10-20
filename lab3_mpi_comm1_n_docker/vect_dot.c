#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ROOT 0

void parse_cmd_args(int argc, char **argv, int *verbose, int *vect_size) {
  for (int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-v") == 0) {
      *verbose = 1;
    } else if (strcmp(argv[i], "--size") == 0) {
      *vect_size = atoi(argv[++i]);
      continue;
    }
  }
}

int main(int argc, char **argv) {
  int vect_size = 9;

  unsigned long int *vec1_sendbuf = NULL;
  unsigned long int *vec2_sendbuf = NULL;

  unsigned long int loc_dot = 0;
  unsigned long int reduced_dot = 0;

  int data_per_worker;

  int world_size, world_rank;

  double t_start, t_end;

  int i;

  // controls whether workers print to the console or not
  int verbose = 0;

  parse_cmd_args(argc, argv, &verbose, &vect_size);

  MPI_Init(NULL, NULL);
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

  // calculate how to split the data equally over the workers
  if (vect_size % world_size == 0) {
    data_per_worker = vect_size / world_size;
  } else {
    // STOP EXECUTION IF NOT POSSIBLE
    if (world_rank == ROOT)
      printf(
          "Vector size of %d cannot be equally distributed over %d "
          "processes!\n",
          vect_size, world_size);
    MPI_Finalize();
    return 0;
  }

  // Allocate memory for receive buffers
  unsigned long int *vec1_recvbuf =
      (unsigned long int *)malloc(data_per_worker * sizeof(unsigned long int));
  unsigned long int *vec2_recvbuf =
      (unsigned long int *)malloc(data_per_worker * sizeof(unsigned long int));

  if (world_rank == ROOT) {
    // Allocate memory for send buffers
    vec1_sendbuf =
        (unsigned long int *)malloc(vect_size * sizeof(unsigned long int));
    vec2_sendbuf =
        (unsigned long int *)malloc(vect_size * sizeof(unsigned long int));

    // Timestamp the starting time of the MPI program to calculate its execution
    // time
    t_start = MPI_Wtime();

    // Initialize the vectors on the root process
    for (i = 0; i < vect_size; i++) {
      vec1_sendbuf[i] = i;
      vec2_sendbuf[i] = i;
    }
  }

  // Scatter the data from the root to all workers
  MPI_Scatter(vec1_sendbuf, data_per_worker, MPI_UNSIGNED_LONG, vec1_recvbuf,
              data_per_worker, MPI_UNSIGNED_LONG, ROOT, MPI_COMM_WORLD);
  MPI_Scatter(vec2_sendbuf, data_per_worker, MPI_UNSIGNED_LONG, vec2_recvbuf,
              data_per_worker, MPI_UNSIGNED_LONG, ROOT, MPI_COMM_WORLD);

  if (verbose) {
    // Print the received data on each process
    printf("Process %d received data: [", world_rank);
    for (i = 0; i < data_per_worker; i++) printf("%lu ", vec1_recvbuf[i]);
    printf("] & [");
    for (i = 0; i < data_per_worker; i++) printf("%lu ", vec2_recvbuf[i]);
    printf("]\n");
    sleep(1);
  }

  // Compute the local dot product in each processes
  for (i = 0; i < data_per_worker; i++) {
    loc_dot += vec1_recvbuf[i] * vec2_recvbuf[i];
  }

  if (verbose) {
    printf("Process %d got a local dot prod of: %lu \n", world_rank, loc_dot);
    sleep(1);
  }

  // Perform the reduction operation so that root receives the final dot product
  MPI_Reduce(&loc_dot, &reduced_dot, 1, MPI_UNSIGNED_LONG, MPI_SUM, ROOT,
             MPI_COMM_WORLD);

  if (world_rank == ROOT) {
    // Timestamp the end of the opperation in order to calculate the execution
    // time
    t_end = MPI_Wtime();

    sleep(1);  // Ensure the following get printed last

    printf("ROOT received the reduced dot product: %lu\n", reduced_dot);
    printf("Execution time: %f seconds\n", t_end - t_start);
  }

  // Free dynamically allocated memory
  if (world_rank == ROOT) {
    free(vec1_sendbuf);
    free(vec2_sendbuf);
  }
  free(vec1_recvbuf);
  free(vec2_recvbuf);

  // Finalise MPI
  MPI_Finalize();

  return 0;
}