#!/bin/bash


###Shell script for running directive.py once


### define resources needed:
### walltime - how long you expect the job to run
#PBS -l walltime=06:00:00

### nodes:ppn - how many nodes & cores per node (ppn) that you require
#PBS -l nodes=1:ppn=1,feature=intel16

### mem: amount of memory that the job will need
#PBS -l mem=4gb

#PBS -A ptg

### you can give your job a name for easier identification
#PBS -N /mnt/home/f0004519/parameter_study/run_directive

### load necessary modules, e.g.
module purge
module load Intel/16.3
module load OpenMPI/2.0.1
module load HDF5/1.8.18

module unload python

export PATH="/mnt/home/f0004519/anaconda3/bin:$PATH"

### change to the working directory where your code is located
cd /mnt/home/f0004519/parameter_study/

### put job id in file
echo ${PBS_JOBID} > directive_jobid.txt

### call your executable
python directive.py 
~                                                                                                                       
~                                                                                                                       
