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
path = "./"
paramFile = os.path.join(path,"positions_new.txt")
param = np.loadtxt(paramFile)
alphaL = param[:,0]
alphaD = param[:,1]

runname = "mcmcPS"
restart = False
mcmcRun = "1"

i = 1
for a,b in zip(alphaL,alphaD):
    path1 = "run_"+runname+"_"+str(i)+"_a"+str(a)+"_b"+str(b) # Sets the name of the run.
    filename = "run.mlt"
    fullpath = os.path.join(path1, filename)

    cmd = "qsub " + fullpath

    print(cmd)
    os.system(cmd)
    i = i + 1
