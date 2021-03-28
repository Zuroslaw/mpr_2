#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --constraint="intel"
#SBATCH --time=00:02:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr21zeus

cd /people/plgzuroslaw/mpr_2 || exit

module add plgrid/tools/openmpi
mpicc -std=c99 -o mc_p mc_p.c
echo "costam"
#python3 ./run.py ./mc_p 10