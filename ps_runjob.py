#!/usr/bin/env python
# ----------------------------------------------------------------
# To run all of the job files created by ps_setup.py
# ----------------------------------------------------------------

import sys
import os
import numpy as np
from settings import *

# ----------------------------------------
#  We will want to read in all of the
#  alpha values from input files.
# ----------------------------------------
#path = "/mnt/research/SNAPhU/STIR/run_ps/"

pathBase = "mcmc_step" + str(mcmc_step)
paramFile = os.path.join(pathBase,"positions_cp.txt")
param = np.loadtxt(paramFile)
alphaL = param[:,0]
alphaD = param[:,1]

i = 1
for a,b in zip(alphaL,alphaD):
    path1 = "run_"+runname+"_a"+str(a)+"_b"+str(b) # Sets the name of the run.
    path2 = os.path.join(pathBase,path1)
    filename = "run.mlt"
    fullpath = os.path.join(path2, filename)

    cmd = "qsub " + fullpath

    print cmd
    os.system(cmd)
    i = i + 1
