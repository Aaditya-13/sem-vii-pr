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
