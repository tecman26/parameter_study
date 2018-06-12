#!/usr/bin/env python

############################################################################
#
# Script Name: mcmc_check.py
# Version 0.0 (June 2018)
# Authors: Theo Cooper and Brandon Barker
#
# Description: For use in paramter studies for the mixing length parameter
# and diffusion parameters for matching 1D models to 3D data. This
# calculates the $\chi^2$ values and gets the accepted new alpha values.
#
############################################################################

from scipy.stats import chisquare
import numpy as np
import numpy.random as npr
import sys, os
from optparse import OptionParser
import glob
import helper_functions
from settings import *
from read3d import *
from read1d import *

if __name__ == '__main__':

    ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]

    print('\n************************************')
    print('**          %s ' % ScriptName )
    print('************************************\n')

    dataDir = "./data"
    path = "./"

    # ---------------------
    # Read 3D Data
    # ---------------------
    data_array, r_sh = read3d(dataDir)


    # ---------------------------------------------------------------
    # Read Prev. 1D Data
    # A Very Bad Solution. Will hopefully replace much of this with
    # function calls. Probably a better way to handle all of the data.
    # ---------------------------------------------------------------

    # For previous step. Replace with function later.
    pathBase_prev = "mcmc_step" + str(mcmc_step - 1)
    paramFile_prev = os.path.join(pathBase_prev,"positions_cp.txt")
    param_prev = np.loadtxt(paramFile_prev)

    alphaL_prev = param_prev[:,0]
    alphaD_prev = param_prev[:,1]

    # For Current Step
    pathBase = "mcmc_step" + str(mcmc_step)
    paramFile = os.path.join(pathBase,"positions_cp.txt")
    param = np.loadtxt(paramFile)

    alphaL = param[:,0]
    alphaD = param[:,1]

    radius_prev = [0]*512
    v_con_prev = [0]*512
    entr_prev = [0]*512
    ye_prev = [0]*512

    radius = [0]*512
    v_con = [0]*512
    entr = [0]*512
    ye = [0]*512

    # ---------------------
    # Read Prev 1D Data
    # ---------------------
    i = 0
    for a,b in zip(alphaL_prev,alphaD_prev):

        path1 = "run_"+runname+"_a"+str(a)+"_b"+str(b)
        path2 = os.path.join(pathBase_prev,path1)
        radius_prev[i], v_con_prev[i], entr_prev[i], ye_prev[i] = read1d(path2)

        i = i + 1

    # ---------------------
    # Read Current 1D Data
    # ---------------------
    i = 0
    for a,b in zip(alphaL,alphaD):

        path1 = "run_"+runname+"_a"+str(a)+"_b"+str(b)
        path2 = os.path.join(pathBase,path1)
        radius[i], v_con[i], entr[i], ye[i] = read1d(path2)

        i = i + 1

    # ---------------------
    # Calc. chi^2 values
    # ---------------------

    chisq_entr = chisquare( [radius, entr], [ data_array[:,0], data_array[:,1] ] )

    # ---------------------
    # eps = sum(chi^2)
    # ---------------------

    # ---------------------
    # read in old error
    # ---------------------

    # ---------------------
    # P = exp( eps_o+eps_n)
    # ---------------------

    # ---------------------
    # assign new alphas
    # ---------------------


    # ---------------------
    # Write Alphas
    # ---------------------
