#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --constraint="intel"
#SBATCH --time=20:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr21zeus

pwd
module add plgrid/tools/openmpi
mpicc -std=c99 -o mc_p mc_p.c

python3 ./run.py ./mc_p 10