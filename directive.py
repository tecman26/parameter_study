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

from scipy.stats import chisquare
import numpy as np
import sys, os
from optparse import OptionParser
import glob
import helper_functions

#import ps_setup

# import yt?

# This "gets" the program name and assigns it to a variable.
ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]


if __name__ == '__main__':
    # Put initialization stuff here. Define timestep etc etc etc

    # This prints the program name. Not necessary, put nice to do
    # before other output. Stylish.

    print('\n************************************')
    print('**          %s ' % ScriptName )
    print('************************************\n')

    
    #----Read in 3D simulation data for comparison----#
    
    dataDir = "./data/"

    r_sh_3D, r, v_con_3D, y_e_3D, s_3D = readOutput(dataDir, 3)


    #----specify which walker step is being run----#
    
    step_num = input("Enter step number")
    output_directory = "/mnt/research/SNAPhU/STIR/run_ps/trial0/step"+str(step_num)
    
    input_directory = "/mnt/research/SNAPhU/STIR/run_ps/trial0/step"+str(step_num-1)
    
    
    positions_filename_ref = input_directory+"/positions.txt"
    
    if input_directory != "none" or os.path.isdir(input_directory) == False:
        print("Please enter a valid step number")
        return
    elif os.path.isfile(positions_filename_ref) == False:
        print("No 'positions.txt' file found")
        return
    

        
    #----Read in previous simulation data----#

    # --------------------------------------------------------------------------------------
    #  positions.txt format:
    #  1, alpha_lambda_1, alpha_d_1
    #  2, alpha_lambda_2, alpha_d_2
    #  ... 
    #  i, alpha_lambda_i, alpha_d_i
    #
    #  for num_walkers lines
    # --------------------------------------------------------------------------------------
    # integrated_data_i.txt format:
    # r (km), v_con (km/s), y_e_prof_prev, s_prof_prev
    # --------------------------------------------------------------------------------------

    sim_dict, positions_prev = readPositions(positions_filename_ref)
    
    num_walkers = len(positions_prev) #number of Markov chain walkers
    num_parameters = len(positions_prev[0]) #number of parameters being varied
        
    #dictionary relating simulation number to positions and list containing tuples of positions

    
    #----Loop for generating guess positions----#
    
    parameter_guess_list = []
    
    for i in range(1,num_walkers+1):
        #In this loop, 'alpha' is left out of variable names to save space
        
        lambda_step = 0.03
        d_step = 0.03
        
        #Pull previous parameter positions
        lambda_prev = sim_dict[i][0]
        d_prev = sim_dict[i][1]

        lambda_guess = lambda_prev + np.random(-lambda_step, lambda_step)
        d_guess = d_prev + np.random(-d_step, d_step)
        
        parameter_guess_list.append([lambda_guess, d_guess])
    
    #----Write guess positions to file----#
    
    writePositions(output_directory, parameter_guess_list) #See helper_functions.py for documentations
    
    #----Set up and run batch of simulations----#
    
    command = "./ps_setup.py"
    print(command)
    os.system(command)
    
    
    
    #----Read and compare results of simulations----#
    
    for i in range(num_walkers):
        
        #glob function returns a list that should have only one file (the one with sim_num = i)
        prev_data_pathname = glob.glob(os.path.join(input_directory,"run_mcmcPS_"+str(i)+"*"))
        prev_data_pathname = prev_data_pathname[0]
        
        guess_data_pathname = glob.glob(os.path.join(output_directory,"run_mcmcPS_"+str(i)+"*"))
        guess_data_pathname = guess_data_pathname[0]
        
        
        r_sh_prev, r_prev, v_con_prev, y_e_prev, s_prev = readOutput(prev_data_pathname, 1)
        r_sh_guess, r_guess, v_con_guess, y_e_guess, s_guess = readOutput(guess_data_pathname, 1)
        
        
        

        #----Metropolis-Hastings Algorithm----#

        


        

        alpha_lambda_guess = 




    next_positions = [] #initialize next position array
    

    

        
