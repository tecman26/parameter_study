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
import helper_functions

#import ps_setup

# This "gets" the program name and assigns it to a variable.
ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]

if __name__ == '__main__':

    # This prints the program name. Not necessary, put nice to do
    # before other output. Stylish.

    print('\n************************************')
    print('**          %s ' % ScriptName )
    print('************************************\n')

    #output_directory = "/mnt/research/SNAPhU/STIR/run_ps/trial0/step0"
    output_directory = "."
    
    #----Hard-coded results from single-parameter alpha_lambda study----#
    
    #pathname_sing = "" #path name for single-parameter study output

    #r_sh_sing, r_sing, v_con_sing, y_e_sing, s_sing = readOutput(pathname_sing)
    
    #-------------------------------------------------------------------#
    # WE NEED CODE HERE TO FIGURE OUT HOW TO INCORPORATE THE RESULTS OF
    # THE PREVIOUS PARAMETER STUDY THAT MACKENZIE DID
    #-------------------------------------------------------------------#

    num_walkers = 1 #IMPORTANT PARAMETER: this determines how many simulations to set up
    next_positions = []
    
    alpha_lambda_min = 0
    alpha_lambda_max = 2 # We can narrow these down once we have data from the previous alpha_lambda parameter study

    #----Generate array of random starting points----#
    alpha_lambda_range = (alpha_lambda_min,alpha_lambda_max)
    alpha_d_range = (0,1)

    for i in range(num_walkers):
        alpha_lambda = (alpha_lambda_max-alpha_lambda_min)*np.random.random_sample() + alpha_lambda_min
        alpha_d = np.random.random_sample() #no multiplier or shift, since range is 0,1 (can change later if necessary)

        next_positions.append([alpha_lambda, alpha_d])

    #----Output positions file----#
    
    positions_filename_out = os.path.join(output_directory,"positions.txt")
    with open(positions_filename_out, "w+") as f:
        for i in range(0,num_walkers):
            f.write(("%d" % (i+1)).rstrip('\n'))
            parameters = next_positions[i]
            for parameter in parameters:
                f.write((", %f" % parameter).rstrip('\n'))
            f.write('\n')

    #----Set up next simulation----#
    
    command = "./ps_setup.py"
    print(command)
    os.system(command)

        