#include <stdio.h>
#include <mpi.h>

#define N 8

int main(int argc, char *argv[])
{
    int rank, size;
    int array[N] = {1, 2, 3, 4, 5, 6, 7, 8};
    int local_array[N];
    int elements_per_process;
    int local_sum = 0;
    int total_sum = 0;
    int i;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (N % size != 0)
    {
        if (rank == 0)
            printf("Use a number of processes that divides %d.\n", N);
        MPI_Finalize();
        return 1;
    }

    elements_per_process = N / size;

    MPI_Scatter(array, elements_per_process, MPI_INT,
                local_array, elements_per_process, MPI_INT,
                0, MPI_COMM_WORLD);

    for (i = 0; i < elements_per_process; i++)
        local_sum += local_array[i];

    printf("Processor %d intermediate sum = %d\n", rank, local_sum);

    MPI_Reduce(&local_sum, &total_sum, 1, MPI_INT, MPI_SUM,
               0, MPI_COMM_WORLD);

    if (rank == 0)
        printf("Final sum = %d\n", total_sum);

    MPI_Finalize();
    return 0;
}
