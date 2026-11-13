# Practical 3: Sum of Array Elements Using OpenMP

## Aim

To find the sum of an array by distributing its elements among parallel threads,
display each thread's intermediate sum, and combine those sums to get the final
result.

## Theory

OpenMP (Open Multi-Processing) is an API for shared-memory parallel programming
in C, C++, and Fortran. It uses compiler directives, runtime functions, and
environment variables to control parallel execution. In C, directives start
with `#pragma omp`. GCC enables OpenMP directives and links its runtime when
compiled with `-fopenmp`. See the [GCC OpenMP documentation](https://gcc.gnu.org/onlinedocs/gcc/OpenMP.html).

This program creates four threads to process an array of eight values. The
`omp for` directive divides the loop iterations among those threads. Each
thread calculates and prints its intermediate sum. An `atomic` directive
protects the addition of each local sum to the shared final sum.

Unlike MPI, OpenMP uses threads that share the same process memory. This code
uses OpenMP `#pragma` directives; it does not use MPI or `mpi.h`.

## Files and roles

| File | Role |
|---|---|
| `omp_sum.c` | Creates the array, divides work among OpenMP threads, prints intermediate sums, and prints the final sum. |

## Program

### `omp_sum.c`

```c
#include <stdio.h>
#include <omp.h>

#define N 8
#define THREADS 4

int main(void)
{
    int array[N] = {1, 2, 3, 4, 5, 6, 7, 8};
    int total_sum = 0;
    int i;

    omp_set_dynamic(0);

    #pragma omp parallel num_threads(THREADS)
    {
        int thread_id = omp_get_thread_num();
        int local_sum = 0;

        #pragma omp for schedule(static, 2)
        for (i = 0; i < N; i++)
            local_sum += array[i];

        printf("Thread %d intermediate sum = %d\n", thread_id, local_sum);

        #pragma omp atomic
        total_sum += local_sum;
    }

    printf("Final sum = %d\n", total_sum);
    return 0;
}
```
| Line(s) | Explanation |
|---|---|
| 1 | Includes standard input/output functions such as `printf`. |
| 2 | Includes the OpenMP runtime declarations, including `omp_get_thread_num`. |
| 4 | Sets the array length to 8. |
| 5 | Requests four OpenMP threads. |
| 7-8 | Declares the program entry point and opens its body. |
| 9 | Creates the array containing the values to sum. |
| 10 | Initializes the shared final sum to zero. |
| 11 | Declares the loop counter used by the work-sharing loop. |
| 13 | Disables dynamic adjustment of the thread count so the requested four threads are used. |
| 15-16 | `parallel` starts the requested team of threads and opens the parallel region. |
| 17 | Gets the ID of the current thread, from 0 to 3. |
| 18 | Initializes this thread's private intermediate sum to zero. |
| 20 | `omp for` divides loop iterations among the threads; `static, 2` assigns two consecutive iterations per chunk. |
| 21-22 | Loops through the array indices assigned to this thread and adds those values to its local sum. |
| 24 | Displays this thread's intermediate sum. The order of output lines can vary. |
| 26-27 | `atomic` makes each thread's addition to the shared `total_sum` safe from simultaneous updates. |
| 28 | Closes the parallel region; all threads have completed before execution continues. |
| 30 | Prints the combined sum after all threads have added their local sums. |
| 31 | Returns success from `main`. |
| 32 | Closes `main`. |

## How to compile and run

This computer has two MinGW GCC installations. The `gcc` command on the normal
PATH is an older compiler whose OpenMP link step fails because it cannot find
`-lpthread`. Code::Blocks' GCC 14.2 installation compiled and ran this program
successfully. In PowerShell, from this folder, use:

```powershell
$ompRunPath = 'C:\Program Files\CodeBlocks\MinGW\bin;' + $env:PATH
$env:PATH = $ompRunPath
& 'C:\Program Files\CodeBlocks\MinGW\bin\gcc.exe' -fopenmp omp_sum.c -o omp_sum.exe
.\omp_sum.exe
```

`-fopenmp` enables the `#pragma omp` directives and links the OpenMP runtime.
The PATH adjustment puts Code::Blocks' matching runtime DLLs before the older
MinGW DLLs already on the normal PATH. GCC documents `-fopenmp` as the option
that enables OpenMP directives and links its runtime ([GCC documentation](https://gcc.gnu.org/onlinedocs/gcc/OpenMP-and-OpenACC-Options.html)).

## Expected result

With four threads, each thread processes two values:

| Thread | Values | Intermediate sum |
|---:|---|---:|
| 0 | 1, 2 | 3 |
| 1 | 3, 4 | 7 |
| 2 | 5, 6 | 11 |
| 3 | 7, 8 | 15 |

The final sum is `3 + 7 + 11 + 15 = 36`. The order of intermediate output lines
may vary. This program was compiled and run with the Code::Blocks GCC 14.2
installation available on this computer; it printed the four intermediate
sums and `Final sum = 36`.

## Execution flow to remember

1. Create the array and initialize the shared total.
2. Start four threads with `#pragma omp parallel`.
3. Divide the loop with `#pragma omp for` and calculate one local sum per thread.
4. Add each local sum safely to the shared total with `#pragma omp atomic`.
5. Print the final sum after the parallel region ends.

## Viva questions and short answers

1. **What is OpenMP?**  
   OpenMP is an API for shared-memory parallel programming in C, C++, and Fortran.

2. **What does `#pragma omp parallel` do?**  
   It creates a team of threads that execute the enclosed parallel region.

3. **What does `#pragma omp for` do?**  
   It divides loop iterations among the threads in the current team.

4. **What is a thread ID?**  
   It is the number identifying a thread in the team; this program gets it using
   `omp_get_thread_num()`.

5. **Why does each thread have a `local_sum`?**  
   Each thread needs its own intermediate total for the values it processes.

6. **Why is `#pragma omp atomic` used?**  
   It prevents simultaneous updates from corrupting the shared `total_sum`.

7. **What does `omp_set_dynamic(0)` do?**  
   It disables dynamic adjustment of the number of threads for a parallel region.

8. **What does `schedule(static, 2)` mean here?**  
   It assigns loop iterations in fixed chunks of two to the threads.

9. **How is OpenMP different from MPI?**  
   OpenMP uses threads that share memory within a process; MPI uses separate
   processes that communicate by passing messages.

10. **What compiler option enables OpenMP in GCC?**  
    Use `-fopenmp` when compiling and linking the program.
