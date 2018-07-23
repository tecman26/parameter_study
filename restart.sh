#!/bin/bash


###Shell script for running calibration simulations


### define resources needed:
### walltime - how long you expect the job to run
#PBS -l walltime=10:00:00

### nodes:ppn - how many nodes & cores per node (ppn) that you require
#PBS -l nodes=4:ppn=8,feature=intel16

### mem: amount of memory that the job will need
#PBS -l mem=10gb

#PBS -A ptg

### you can give your job a name for easier identification
#PBS -N /mnt/research/SNAPhU/STIR/parameter_study/restart

#PBS -M tecnerd3@gmail.com
#PBS -m abe

### load necessary modules, e.g.
module purge
module load Intel/16.3
module load OpenMPI/2.0.1
module load HDF5/1.8.18

module unload python

export PATH="/mnt/home/f0004519/anaconda3/bin:$PATH"

### change to the working directory where your code is located
cd /mnt/research/SNAPhU/STIR/parameter_study/

### put job id in file
### echo ${PBS_JOBID} > markov_jobid.txt

cd /mnt/research/SNAPhU/STIR/parameter_study/calib2/run_mcmcPS_48_a0.386667_b0.9/output
mpirun -np 2 flash4

cd /mnt/research/SNAPhU/STIR/parameter_study/calib2/run_mcmcPS_49_a0.43_b0.05/output
mpirun -np 2 flash4



