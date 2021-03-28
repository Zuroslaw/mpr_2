import sys
import os
import shutil
from datetime import datetime

exec_path = sys.argv[1]  # path to compiled monte-carlo program
repeats_series = int(sys.argv[2])  # number of repeats of experiment for series (1-12 nodes)

if os.path.exists("./results"):
    shutil.rmtree("./results")

os.mkdir("./results")

big_size = 23950080000  # 50 * 12! ~ 80 sekund dla 12 watkow
small_size = 23950080  # 12! / 20 ~ 0,9 sekundy dla 1 watku
medium_size = 757368029  # ~ sqrt(big_size * small_size) = ~ 24s dla 12 watkow

# estimated experiment time:
# strong:
# small: (1/12 + 1/11 + ... + 1/1) ~ 3,1 -> 0,9 * 3,1 = 2,8s -> 2,8 * 10 repeats = 28s
# medium: 12/(1 + 2 ... + 12) ~ 12 * 3,1 = 37,2 -> 37,2 * 24 = 893 s * 10 repeats = 8930s
# big: 12/(1 + 2 ... + 12) ~ 12 * 3,1 = 37,2 -> 37,2 * 80 = 2976 s * 10 repeats = 29760s
# weak:
# small: 0,9 * 12 = 10,8s -> 10,8 * 10 repeats -> < 108s
# medium: 24s * 12 = 288s -> 288 * 10 repeats -> 2880s
# big: 80s * 12 = 960s -> 960s * 10 repeats -> 9600s
# total: ~ 14,25h


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


f = open("experiment.txt", "a")
f.write("start: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
f.close()

strong(small_size, "small")
strong(medium_size, "medium")
strong(big_size, "big")

weak(small_size, "small")
weak(medium_size, "medium")
weak(big_size, "big")

f = open("experiment.txt", "a")
f.write("\nend: ")
f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
f.close()
