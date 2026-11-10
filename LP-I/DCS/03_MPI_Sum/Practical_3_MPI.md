# Practical 3: Sum of Array Elements Using MPI

## Aim

To find the sum of an array by dividing its elements among MPI processes,
display each process's intermediate sum, and combine the intermediate sums to
get the final result.

## Theory

MPI stands for **Message Passing Interface**. It is a standard library for
writing programs that run as multiple processes and communicate by passing
data. Each process runs the same program and is identified by a **rank**. The
total number of processes is called the **size** of the communicator.

This program has an array of eight values and is run with four processes. Each
process receives `N / size`, or two, values using `MPI_Scatter`. It calculates
its own local sum, prints that intermediate result, and then all processes call
`MPI_Reduce` with `MPI_SUM` to add their local sums together. Process 0 receives
and prints the final sum.

The version in the ZIP distributes uneven array sizes too, using `MPI_Scatterv`
and extra count and displacement arrays. This study version uses a fixed array
and equal-sized partitions to make the main MPI ideas easier to remember. The
number of processes must divide 8; run it with four processes as shown below.

## Files and roles

| File | Role |
|---|---|
| `mpi_sum.c` | Creates the array, distributes values, calculates intermediate sums, and reduces them to the final sum. |

## Program

### `mpi_sum.c`

```c
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
```
| Line(s) | Explanation |
|---|---|
| 1 | Includes standard input/output functions such as `printf`. |
| 2 | Includes MPI declarations and function prototypes. |
| 4 | Sets the array length to 8. |
| 6-7 | Declares the program entry point and opens its body. MPI may update the command-line arguments during initialization. |
| 8 | Declares `rank` (this process's ID) and `size` (the total process count). |
| 9 | Creates the eight-element array. The root process supplies this array to `MPI_Scatter`. |
| 10 | Reserves space for the values received by this process. Only the first `elements_per_process` entries are used. |
| 11 | Stores how many array values each process receives. |
| 12 | Initializes this process's partial sum to zero. |
| 13 | Declares the variable that will receive the final sum on process 0. |
| 14 | Declares the loop counter. |
| 16 | Starts the MPI environment; every process must call this before other MPI functions. |
| 17 | Gets this process's rank in `MPI_COMM_WORLD`. |
| 18 | Gets the number of processes in `MPI_COMM_WORLD`. |
| 20-26 | Checks that the process count divides 8 evenly. If it does not, process 0 prints a message, all processes finalize MPI, and the program exits. |
| 28 | Calculates the equal number of elements assigned to each process. With 8 values and 4 processes, this is 2. |
| 30-32 | `MPI_Scatter` divides the root's array into equal chunks and sends one chunk to each process. All processes call this collective operation; `0` identifies the root. |
| 34-35 | Adds the values received by this process to its local sum. |
| 37 | Prints this process's rank and intermediate sum. The order of these lines can vary. |
| 39-40 | `MPI_Reduce` combines every process's local sum with `MPI_SUM`; process 0 receives the total in `total_sum`. |
| 42-43 | Only rank 0 prints the final result. |
| 45 | Ends the MPI environment; every process calls this before exiting. |
| 46-47 | Returns success and closes `main`. |

## How to compile and run

Use an MPI-enabled environment. In an Open MPI or MPICH terminal, compile with:

```sh
mpicc mpi_sum.c -o mpi_sum
```

Run four processes:

```sh
mpirun -n 4 ./mpi_sum
```

Some MPI installations use `mpiexec` instead of `mpirun`; use the launcher
provided by the environment. Open MPI documents the wrapper compiler and the
`mpirun -n <process-count>` pattern in its [build guide](https://docs.open-mpi.org/en/main/building-apps/index.html)
and [launch quick start](https://docs.open-mpi.org/en/main/launching-apps/quickstart.html).

The current workspace terminal does not have `mpicc`, `mpirun`, or `mpiexec` on
its PATH, so this program has not been compiled or run here. Use the MPI-enabled
environment provided by your practical lab.

## Expected result

With four processes, each gets two values:

| Process | Values received | Intermediate sum |
|---:|---|---:|
| 0 | 1, 2 | 3 |
| 1 | 3, 4 | 7 |
| 2 | 5, 6 | 11 |
| 3 | 7, 8 | 15 |

The final sum is `3 + 7 + 11 + 15 = 36`. The intermediate output lines may
appear in a different order on different runs.

## Execution flow to remember

1. Start MPI and get each process's rank and the total process count.
2. Divide the array evenly and scatter each chunk from process 0.
3. Calculate and display one local sum per process.
4. Reduce all local sums using `MPI_SUM` to process 0.
5. Print the final sum and shut down MPI.

## Viva questions and short answers

1. **What is MPI?**  
   MPI is the Message Passing Interface, a standard library for communication
   between processes in parallel programs.

2. **What is a process rank?**  
   It is the unique ID of a process in a communicator, from 0 to `size - 1`.

3. **What does `MPI_COMM_WORLD` represent?**  
   It is the communicator containing all processes started for this program.

4. **What does `MPI_Comm_size` return?**  
   It returns the number of processes in the communicator.

5. **What does `MPI_Scatter` do?**  
   It divides data at the root and sends an equal-sized part to each process.

6. **What is the root process in this program?**  
   Rank 0; it provides the array and receives the final sum.

7. **What does `MPI_Reduce` do here?**  
   It combines all local sums using `MPI_SUM` and stores the total at rank 0.

8. **Why must the number of processes divide 8 in this version?**  
   `MPI_Scatter` sends the same number of elements to every process, so the
   array is split into equal chunks.

9. **Why can the intermediate sums print in different orders?**  
   Processes run independently, and their output timing is not fixed.

10. **Why do all processes call `MPI_Finalize`?**  
    It shuts down the MPI environment for each participating process.
