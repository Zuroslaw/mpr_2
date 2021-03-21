#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void monte_carlo(long long size) {
    srand(time(0));
    long circle_points = 0;
    long square_points = size;

    while (size --> 0) {
        double x = (double) rand() / (double) RAND_MAX;
        double y = (double) rand() / (double) RAND_MAX;

        if (x*x + y*y <= 1.0)
            circle_points++;
    }

    double pi = 4*((double) circle_points / (double) square_points);
    printf("%f", pi);
}

int main(int argc, char * argv[]) {
    char* endptr;
    long long size = strtoll(argv[1], &endptr, 10);
    monte_carlo(size);
}