#!/usr/bin/env python

############################################################################
#
# Script Name: primer.py
# Version 0.0 (June 2018)
# Authors: Theo Cooper and Brandon Barker
#
# Description: For use in parameter studies for the mixing length parameter
# and diffusion parameters for matching 1D models to 3D data. Generates
# intitial set of num_walkers simulations and primes simulation files.
#
############################################################################

from scipy.stats import chisquare
import numpy as np
import sys, os
from optparse import OptionParser
import glob
#import readData1D
#import ps_setup

# This "gets" the program name and assigns it to a variable.
ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]

if __name__ == '__main__':

    # This prints the program name. Not necessary, put nice to do
    # before other output. Stylish.

    print('\n************************************')
    print('**          %s ' % ScriptName )
    print('************************************\n')

    output_directory = "/mnt/research/SNAPhU/STIR/run_ps/trial0/step0"
    
    
      #----Hard-coded results from single-parameter alpha_lambda study----#

        # v_con_sing = 
        # r_sh_sing = 
        # y_e_prof_sing = 
        # s_prof_sing =
    
        alpha_lambda_min = 0
        alpha_lambda_max = 2 # We can narrow these down once we have data from the previous alpha_lambda parameter study
        
        #----Generate array of random starting points----#
        alpha_lambda_range = (alpha_lambda_min,alpha_lambda_max)
        alpha_d_range = (0,1)
        
        for i in range(num_walkers):
            alpha_lambda = (alpha_lambda_max-alpha_lambda_min)*np.random.random_sample() + alpha_lambda_min
            alpha_d = np.random.random_sample() #no multiplier or shift, since range is 0,1 (can change later if necessary)
            
            next_positions.append((alpha_lambda, alpha_d))
            
        next_positions = np.array(next_positions)