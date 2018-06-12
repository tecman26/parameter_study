#!/usr/bin/env python

############################################################################
#
# Script Name: mcmc_check.py
# Version 0.0 (June 2018)
# Authors: Theo Cooper and Brandon Barker
#
# Description: For use in paramter studies for the mixing length parameter
# and diffusion parameters for matching 1D models to 3D data.
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

    # ---------------------
    # Read Prev. 1D Data
    # ---------------------



    # ---------------------
    # Read Current 1D Data
    # ---------------------


    # ---------------------
    # Calc. chi^2 values
    # ---------------------

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
