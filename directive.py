#!/usr/bin/env python

############################################################################
#
# Script Name: directive.py
# Version 0.0 (June 2018)
# Authors: Theo Cooper and Brandon Barker
#
# Description: For use in paramter studies for the mixing length parameter
# and diffusion parameters for matching 1D models to 3D data.
#
############################################################################

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
    print('**          MCMC Step %d ' % mcmc_step )
    print('************************************\n')

    if ( mcmc_step < nSteps ):

        dataDir = "./data"
        path = "./"
        pos_filename = os.path.join(path, "positions.txt") # cumulative list of pairs
        pos_old_filename = os.path.join(path, "positions_old.txt")

        if ( mcmc_step == 1 ):

            next_positions = []

            alpha_l_options = (2)*np.random.random_sample(num_alpha_l) + 0
            alpha_d_options = (1)*np.random.random_sample(num_alpha_d) + 0

            helper_functions.writeParameters(alpha_l_options, alpha_d_options)

            # ------------------------------------------
            # runs the setup and job submission scripts.
            # ------------------------------------------
            cmd = "python ps_setup.py"
            print(cmd)
        #    os.system(cmd)
            cmd = "python ps_runjob.py"
            print(cmd)
            #os.system(cmd)

        # --------------------------------------------------------------
        #  Main Section of the MCMC Implementation
        # --------------------------------------------------------------
        else:

            alphaL_guess = []
            alphaD_guess = []

            # Read in old alphas
            #path = "/mnt/research/SNAPhU/STIR/run_ps/"
            path = "./" # Path to parameter list files.
            paramFile = os.path.join(path,"positions_old.txt") #

            # Read in old values.
            alphaL_old, alphaD_old = helper_functions.getOldAlphas(paramFile)

            # Get new guess values for the alphas
            for i in range(num_alpha_l):
                guess = alphaL_old[i] + npr.uniform(-dA,dA)
                alphaL_guess.append(guess)
            for i in range(num_alpha_d):
                guess = alphaD_old[i] + npr.uniform(-dA,dA)
                alphaD_guess.append(guess)

            # write guesses to positions_old.txt
            helper_functions.writeParameters(alphaL_guess, alphaD_guess)
