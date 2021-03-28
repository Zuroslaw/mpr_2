#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --constraint="intel"
#SBATCH --time=20:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr21zeus


module add plgrid/tools/openmpi

python3 ./run.py ./mc_p 10