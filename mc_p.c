#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>

void monte_carlo(long long points_per_process, int world_rank, int world_size, char* file_name) {

    srand(time(0) * world_rank);

    long long circle_points = 0;
    long long global_circle_points;
    double start;
    double end;

    MPI_Barrier(MPI_COMM_WORLD);
    start = MPI_Wtime();

    for (long long i = 0; i < points_per_process; ++i) {
        double x = (double) rand() / (double) RAND_MAX;
        double y = (double) rand() / (double) RAND_MAX;

        if (x*x + y*y <= 1.0)
            circle_points++;
    }

    MPI_Reduce(&circle_points, &global_circle_points, 1, MPI_LONG_LONG, MPI_SUM, 0, MPI_COMM_WORLD);
    end = MPI_Wtime();


    if (world_rank == 0) {
        long long global_square_points = points_per_process * world_size;
        double pi = 4*((double) global_circle_points / (double) global_square_points);
        printf("\n\n");
        printf("total points = %lld\n", global_square_points);
        printf("pi = %f\n", pi);
        printf("%.*e\n", 10, end - start);
        FILE* fp = fopen(file_name, "a");
        fprintf(fp, "%.*e\n", 10, end - start);
        fclose(fp);
    }
}

int main(int argc, char * argv[]) {
    char* endptr;
    long long size = strtoll(argv[1], &endptr, 10);
    char* file_name = argv[2];

    MPI_Init(NULL, NULL);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    long long points_per_process = size / world_size;

    monte_carlo(points_per_process, world_rank, world_size, file_name);

    MPI_Finalize();
}