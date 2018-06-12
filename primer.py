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

    trial_directory = "/mnt/research/SNAPhU/STIR/run_ps/trial0"
    output_directory = "/mnt/research/SNAPhU/STIR/run_ps/trial0/step0"
    #output_directory = "."
    
    #----Hard-coded results from single-parameter alpha_lambda study----#
    
    #pathname_sing = "" #path name for single-parameter study output

    #r_sh_sing, r_sing, v_con_sing, y_e_sing, s_sing = readOutput(pathname_sing)
    
    #-------------------------------------------------------------------#
    # WE NEED CODE HERE TO FIGURE OUT HOW TO INCORPORATE THE RESULTS OF
    # THE PREVIOUS PARAMETER STUDY THAT MACKENZIE DID
    #-------------------------------------------------------------------#

    #IMPORTANT PARAMETERS: these determines how many simulation walkers to set up
    alpha_lambda_num = 1 # number of alpha_lambda options (for method 2)
    alpha_d_num = 1 # number of alpha_d options (for method 2)
    num_walkers = alpha_lambda_options*alpha_d_options
    
    next_positions = []
    
    #----Generate array of random starting points----#
    
    method = 1
    """Method 1 creates array of totally random starting points within the area. Method 2 creates two arrays with
    16 alpha_lambda values and 32 alpha_d values and takes their Cartesian product"""
    
    alpha_lambda_min = 0
    alpha_lambda_max = 2 # We can narrow these down once we have data from the previous alpha_lambda parameter study
    
    alpha_d_min = 0
    alpha_d_max = 1
    
    alpha_lambda_range = (alpha_lambda_min,alpha_lambda_max)
    alpha_d_range = (alpha_d_min,alpha_d_max)
    
    
    if method == 1:

        for i in range(num_walkers):
            alpha_lambda = (alpha_lambda_max-alpha_lambda_min)*np.random.random_sample() + alpha_lambda_min
            alpha_d = (alpha_d_max-alpha_d_min)*np.random.random_sample() + alpha_d_min

            next_positions.append([alpha_lambda, alpha_d])
            
    else:
        
        alpha_lambda_options = (alpha_lambda_max-alpha_lambda_min)*np.random.random_sample(16) + alpha_lambda_min
        alpha_d_options = (alpha_d_max-alpha_d_min)*np.random.random_sample(32) + alpha_d_min
        
        for i in range(alpha_lambda_options):
            for j in range(alpha_d_options):
                alpha_lambda = alpha_lambda_options[i]
                alpha_d = alpha_d_options[j]
                next_positions.append([alpha_lambda, alpha_d])
       

    #----Output positions file----#
    
    
    writePositions(output_directory, next_positions)
    
            
    #----Output all_positions file----#
    
    #--------------------------------------------------------------
    # all_positions format:
    #--------------------------------------------------------------
    # 1, 2, ..., num_walkers
    # (param_1_1, param_1_2), (param_2_1, param_2_2), ..., (  ) for step 0
    # (param_1_1, param_1_2), (param_2_1, param_2_2), ..., (  ) for step 1
    #--------------------------------------------------------------
    
    positions_filename_out = os.path.join(trial_directory,"all_positions.txt")
    with open(positions_filename_out, "w+") as f:
        for i in range(num_walkers-1):
            f.write(("%d, " % (i+1)).rstrip('\n'))
        f.write("%d\n" % num_walkers)
        for i in range(num_walkers-1):
            parameters = next_positions[i]
            f.write(("(").rstrip('\n'))
            f.write((parameters[0]).rstrip('\n'))
            for parameter in parameters[1:]:
                f.write((", %f" % parameter).rstrip('\n'))
            f.write(("), ").rstrip('\n'))
        parameters = next_positions[num_walkers-1]
        f.write(("(").rstrip('\n'))
        f.write((parameters[0]).rstrip('\n'))
        for parameter in parameters[1:]:
            f.write((", %f" % parameter).rstrip('\n'))
        f.write(")")
            
    #----Set up next simulation----#
    
    command = "./ps_setup.py"
    print(command)
    os.system(command)

        