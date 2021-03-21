#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>

void monte_carlo(long long points_per_process, int world_rank, int world_size) {

    srand(time(0) * world_rank);
    long long circle_points = 0;

    MPI_Barrier(MPI_COMM_WORLD);
    double start = MPI_Wtime();

    for (long long i = 0; i < points_per_process; ++i) {
        double x = (double) rand() / (double) RAND_MAX;
        double y = (double) rand() / (double) RAND_MAX;

        if (x*x + y*y <= 1.0)
            circle_points++;
    }

    long long global_circle_points;
    MPI_Reduce(&circle_points, &global_circle_points, 1, MPI_LONG_LONG, MPI_SUM, 0, MPI_COMM_WORLD);
    double end = MPI_Wtime();


    if (world_rank == 0) {
        long long global_square_points = points_per_process * world_size;
        double pi = 4*((double) global_circle_points / (double) global_square_points);
        printf("\n\n");
        printf("total points = %lld\n", global_square_points);
        printf("pi = %f\n", pi);
        printf("time = %f\n", end - start);
    }
}

int main(int argc, char * argv[]) {
    char* endptr;
    long long size = strtoll(argv[1], &endptr, 10);

    MPI_Init(NULL, NULL);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    printf("Initialized host: %s\n", processor_name);

    long long points_per_process = size / world_size;

    monte_carlo(points_per_process, world_rank, world_size);

    MPI_Finalize();
}