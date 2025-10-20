#include <mpi.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAT_SIZE 500

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
// void print_matrix2D(int rows, int cols, double mat[rows][cols], const char *name)
// {
//   printf("Matrix %s (%d x %d):\n", name, rows, cols);
//   for (int i = 0; i < rows; i++)
//   {
//     for (int j = 0; j < cols; j++)
//     {
//       printf("%8.2f ", mat[i][j]);
//     }
//     printf("\n");
//   }
//   printf("\n");
// }

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

  // 用0补齐不能均分的部分
  int cal_size = mpiSize;
  int Np = ((MAT_SIZE + cal_size - 1) / cal_size) * cal_size; //((N + P - 1) / P) * P;
  int rows_per_rank = Np / cal_size;

  double *a_pad = NULL,*c_pad = NULL;


  if (rank == 0)
  {
    /* root */
    a_pad = (double*)calloc((size_t)Np * MAT_SIZE, sizeof(double));
    c_pad = (double*)malloc((size_t)Np * MAT_SIZE * sizeof(double));
    /* First, fill some numbers into the matrix */
    for (int i = 0; i < MAT_SIZE; i++)
    {
      for (int j = 0; j < MAT_SIZE; j++)
      {
        a[i][j] = i + j;
        b[i][j] = i * j;
      }
    }
    memcpy(a_pad, a, (size_t)MAT_SIZE * MAT_SIZE * sizeof(double));

  }
  double *a_blk  = (double*)malloc((size_t)rows_per_rank * MAT_SIZE * sizeof(double));
  double *c_blk  = (double*)calloc((size_t)rows_per_rank * MAT_SIZE, sizeof(double));
  /* Measure start time */
  double start = MPI_Wtime();

  /* Send matrix data to the worker tasks */

  // a: partial matrix
  MPI_Scatter(a_pad, rows_per_rank * MAT_SIZE, MPI_DOUBLE, a_blk, rows_per_rank * MAT_SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);
  // b: whole matrix
  MPI_Bcast(b, MAT_SIZE*MAT_SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);

  /* Compute its own piece */
  for (int i = 0; i < rows_per_rank; i++)
  {
    for (int j = 0; j < MAT_SIZE; j++)
    {
      for (int k = 0; k < MAT_SIZE; k++)
      {
        c_blk[i*(size_t)MAT_SIZE + j]+=a_blk[i*(size_t)MAT_SIZE + k]* b[k][j];
      }
    }
  }


  /* Gather */

  MPI_Gather(c_blk, rows_per_rank * MAT_SIZE, MPI_DOUBLE, c_pad, rows_per_rank * MAT_SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);

  if (rank == 0)
  {
    /* Receive results from worker tasks */
    // 去掉补齐的部分
    memcpy(c, c_pad, (size_t)MAT_SIZE * MAT_SIZE * sizeof(double));

    /* Measure finish time */
    double finish = MPI_Wtime();
    printf("Done in %f seconds.\n", finish - start);

    /* Compare results with those from brute force */
    double start_bf = MPI_Wtime();
    brute_force_matmul(a, b, bfRes);
    double finish_bf = MPI_Wtime();
    printf("Brute force done in %f seconds.\n", finish_bf - start_bf);
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

  /* Don't forget to finalize your MPI application */
  MPI_Finalize();
}
