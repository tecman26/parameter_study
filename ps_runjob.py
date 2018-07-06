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
def runjob(dir_path):
    #path = "/mnt/research/SNAPhU/STIR/run_ps/"
    #path = "./trial_test/step0"
    paramFile = os.path.join(dir_path,"positions.txt")
    param = np.loadtxt(paramFile, delimiter=",")
    alphaL = param[:,1]
    dneut = param[:,2]
    dye = param[:,3]
    deint = param[:,4]
    detrb = param[:,5]

    runname = "mcmcPS"
    restart = False
    mcmcRun = "1"


    job_id_file = os.path.join(dir_path,"job_ids.txt")
    os.system("touch "+job_id_file)
    
    for i in range(1000,param.shape[0]+1):
        path1 = "run_"+runname+"_"+str(i) # Sets the name of the run.
        filename = "run.mlt"
        fullpath = os.path.join(dir_path, os.path.join(path1, filename))

        #perm = "chmod u+x "+fullpath #give permission
        
        
        cmd = "qsub " + fullpath+" >> "+job_id_file
        #cmd = fullpath

        #os.system(perm)
        #print(cmd)
        os.system(cmd)
        
        
        #os.system("command1 > out.txt 2> err.txt")
        #os.system("command2 -f -z -y > out.txt 2> err.txt")
