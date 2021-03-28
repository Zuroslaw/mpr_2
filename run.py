import sys
import os
import shutil

exec_path = sys.argv[1]
repeats_series = int(sys.argv[2])

os.system("mpiexec -n 4 " + exec_path + " 100 ./out.txt")

if os.path.exists("./results"):
    shutil.rmtree("./results")

os.mkdir("./results")


def run_mpiexec(number_of_nodes, problem_size, file_name):
    file_path = f"./results/{file_name}.txt"
    os.system(f"mpiexec -n {number_of_nodes} {exec_path} {problem_size} {file_path}")


def run_series(problem_size, file_name):
    for number_of_nodes in range(1, 13):
        run_mpiexec(number_of_nodes, problem_size, file_name)


def run_series_repeated(problem_size, file_prefix):
    for i in range(repeats_series):
        run_series(problem_size, f"{file_prefix}_{i}")


run_series_repeated(100, "wynik")

