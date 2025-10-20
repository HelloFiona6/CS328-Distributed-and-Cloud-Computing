#include <mpi.h>
#include <stdio.h>

#define MAT_SIZE 10

void brute_force_matmul(double mat1[MAT_SIZE][MAT_SIZE],
                        double mat2[MAT_SIZE][MAT_SIZE],
                        double res[MAT_SIZE][MAT_SIZE])
{
  /* matrix multiplication of mat1 and mat2, store the result in res */
  for (int i = 0; i < MAT_SIZE; ++i)
  {
    for (int j = 0; j < MAT_SIZE; ++j)
    {
      res[i][j] = 0;
      for (int k = 0; k < MAT_SIZE; ++k)
      {
        res[i][j] += mat1[i][k] * mat2[k][j];
      }
    }
  }
}

int checkRes(const double target[MAT_SIZE][MAT_SIZE],
             const double res[MAT_SIZE][MAT_SIZE])
{
  /* check whether the obtained result is the same as the intended target; if
   * true return 1, else return 0 */
  for (int i = 0; i < MAT_SIZE; ++i)
  {
    for (int j = 0; j < MAT_SIZE; ++j)
    {
      if (res[i][j] != target[i][j])
      {
        return 0;
      }
    }
  }
  return 1;
}
void print_matrix2D(int rows, int cols, double mat[rows][cols], const char *name)
{
  printf("Matrix %s (%d x %d):\n", name, rows, cols);
  for (int i = 0; i < rows; i++)
  {
    for (int j = 0; j < cols; j++)
    {
      printf("%8.2f ", mat[i][j]);
    }
    printf("\n");
  }
  printf("\n");
}

int main(int argc, char *argv[])
{
  int rank;
  int mpiSize;
  double a[MAT_SIZE][MAT_SIZE],  /* matrix A to be multiplied */
      b[MAT_SIZE][MAT_SIZE],     /* matrix B to be multiplied */
      c[MAT_SIZE][MAT_SIZE],     /* result matrix C */
      bfRes[MAT_SIZE][MAT_SIZE]; /* brute force result bfRes */

  /* You need to intialize MPI here */
  MPI_Init(NULL, NULL);
  MPI_Comm_size(MPI_COMM_WORLD, &mpiSize);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  // printf("a sized: %lu * %lu, b sized: %lu * %lu\n", sizeof(a) / sizeof(a[0]), sizeof(a[0]) / sizeof(a[0][0]), sizeof(b) / sizeof(b[0]), sizeof(b[0]) / sizeof(b[0][0]));

  // 用0补齐不能均分的部分
  int cal_size = mpiSize - 1;
  int padding = ((MAT_SIZE + cal_size - 1) / cal_size) * cal_size; //((N + P - 1) / P) * P;
  printf("rank=%d, mpiSize=%d, padding=%d\n", rank, mpiSize, padding);
  double a_pad[padding][MAT_SIZE];
  double c_pad[padding][MAT_SIZE];
  // printf("a_pad sized: %lu * %lu\n", sizeof(a_pad) / sizeof(a_pad[0]), sizeof(a_pad[0]) / sizeof(a_pad[0][0]));
  double a_rcv[padding / cal_size][MAT_SIZE];
  double b_rcv[MAT_SIZE][MAT_SIZE];
  
  if (rank == 0)
  {
    /* root */

    /* First, fill some numbers into the matrix */
    for (int i = 0; i < MAT_SIZE; i++)
    {
      for (int j = 0; j < MAT_SIZE; j++)
      {
        a[i][j] = i + j;
        a_pad[i][j] = a[i][j];
        b[i][j] = i * j;
      }
    }
    print_matrix2D(MAT_SIZE, MAT_SIZE, a, "A original");
    print_matrix2D(MAT_SIZE, MAT_SIZE, b, "B original");

    /* Measure start time */
    double start = MPI_Wtime();

    /* Send matrix data to the worker tasks */

    // a: partial matrix
    MPI_Scatter(&a_pad, padding / cal_size * MAT_SIZE, MPI_DOUBLE, &a_rcv, padding / cal_size * MAT_SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    // b: whole matrix
    MPI_Bcast(&b, MAT_SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    /* Compute its own piece */

    /* Receive results from worker tasks */

    /* Measure finish time */
    double finish = MPI_Wtime();
    printf("Done in %f seconds.\n", finish - start);

    /* Compare results with those from brute force */
    brute_force_matmul(a, b, bfRes);
    if (!checkRes(bfRes, c))
    {
      printf(
          "ERROR: Your calculation is not the same as the brute force result, "
          "please check!\n");
    }
    else
    {
      printf("Result is correct.\n");
    }
  }
  else
  {
    /* worker */

    MPI_Bcast(&a_rcv, padding / cal_size, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&b_rcv, MAT_SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    printf("rank=%d, mpiSize=%d,\n a_rcv sized: %lu * %lu, b_rcv sized: %lu * %lu\n", rank, mpiSize, sizeof(a_rcv) / sizeof(a_rcv[0]), sizeof(a_rcv[0]) / sizeof(a_rcv[0][0]), sizeof(b_rcv) / sizeof(b_rcv[0]), sizeof(b_rcv[0]) / sizeof(b_rcv[0][0]));
    /* Receive data from root and compute, then send back to root */
    print_matrix2D(padding / cal_size, MAT_SIZE, a_rcv, "rcv a");
    print_matrix2D(MAT_SIZE, MAT_SIZE, b_rcv, "rcv b");
  }

  /* Don't forget to finalize your MPI application */
  MPI_Finalize();
}
