import sys
import os
import shutil

exec_path = sys.argv[1]  # path to compiled monte-carlo program
repeats_series = int(sys.argv[2])  # number of repeats of experiment for series (1-12 nodes)

if os.path.exists("./results"):
    shutil.rmtree("./results")

os.mkdir("./results")

big_size = 23950080000  # 50 * 12! ~ 80 sekund dla 12 watkow
small_size = 23950080  # 12! / 20 ~ 0,9 sekundy dla 1 watku
medium_size = 757368029  # ~ sqrt(big_size * small_size)


# runs a single mpiexec for given number of nodes, problem size and saves time to file
def run_mpiexec(number_of_nodes, problem_size, file_name):
    file_path = f"./results/{file_name}.txt"
    os.system(f"mpiexec -n {number_of_nodes} {exec_path} {problem_size} {file_path}")


# runs mpiexec 12 times, incrementing number of nodes on each run
def run_series(sizes, file_name):
    for i in range(12):
        run_mpiexec(i + 1, sizes[i], file_name)


# runs above series specified number of times to get more accurate results
def run_series_repeated(sizes, file_prefix):
    for i in range(repeats_series):
        run_series(sizes, f"{file_prefix}_{i}")


def strong(problem_size, problem_size_name):
    sizes = [problem_size for _ in range(12)]
    run_series_repeated(sizes, f"strong_{problem_size_name}")


def weak(problem_size, problem_size_name):
    sizes = [int(round(problem_size / (12 - i))) for i in range(12)]
    run_series_repeated(sizes, f"weak_{problem_size_name}")


strong(small_size, "small")
weak(small_size, "small")


