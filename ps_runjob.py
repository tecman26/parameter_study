#!/usr/bin/env python
# ----------------------------------------------------------------
# To run all of the job files created by ps_setup.py
# ----------------------------------------------------------------

import sys
import os
import numpy as np

# ----------------------------------------
#  We will want to read in all of the
#  alpha values from input files.
# ----------------------------------------
#path = "/mnt/research/SNAPhU/STIR/run_ps/"
path = "./trial_test/step0"
paramFile = os.path.join(path,"positions.txt")
param = np.loadtxt(paramFile, delimiter=",")
alphaL = param[:,1]
alphaD = param[:,2]

runname = "mcmcPS"
restart = False
mcmcRun = "1"

i = 1
for a,b in zip(alphaL,alphaD):
    path1 = "run_"+runname+"_"+str(i)+"_a"+str(a)+"_b"+str(b) # Sets the name of the run.
    filename = "run.mlt"
    fullpath = os.path.join(path, os.path.join(path1, filename))
    
    #perm = "chmod u+x "+fullpath #give permission CHANGE ONCE IN HPC

    cmd = "qsub " + fullpath #CHANGE ONCE IN HPC
    #cmd = fullpath

    #os.system(perm)
    os.system(cmd)
    #os.system("command1 > out.txt 2> err.txt")
    #os.system("command2 -f -z -y > out.txt 2> err.txt")
    i = i + 1
