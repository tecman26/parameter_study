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

    #----Read in 3D simulation data----#
    # Looks like only the shock radius is in the 3D .txt file.
    # The other variables will have to come from elsewhere.
    # There's also probably a better way to do this reading of data, 
    # but this is fine for now.
    
    dataDir = "./data/"

    r_sh_3D, r, v_con_3D, y_e_3D, s_3D = readOutput(dataDir, 3)

    dirname = "none"
    
    parser = OptionParser()
#    parser.add_option("-r", "--read_dir", action="store", dest="dirname", help="Submit directory from previous batch of simulations")
    
    positions_filename_ref = dirname+"/positions.txt"
    
    if dirname != "none" or os.path.isdir(dirname) == False:
        print("Please enter the name of a valid directory")
        return
    elif os.path.isfile(positions_filename_ref) == False:
        print("No 'positions.txt' file found")
        return
    
    #----specify which walker step is being run----#
    
    step_num = input("Enter step number")
    output_directory = "/mnt/research/SNAPhU/STIR/run_ps/trial0/step"+str(step_num)
        
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

    
    ############################################################################
    #--------------------------------MAIN LOOP---------------------------------#
     ############################################################################
    for i in range(1,num_walkers+1):
        
        #Run batch of simulations from previous positions.txt
        
        
        
        
        data_pathname = str(glob.glob(dirname+"/run_mcmcPS_"+str(i)+"*")) #glob function returns a list that should have only one file (the one with sim_num = i)

        
        


        #----Metropolis-Hastings Algorithm----#

        lambda_step = 0.03
        d_step = 0.03


        #Pull previous parameter positions 
        alpha_lambda_prev = sim_dict[i][0] 
        alpha_d_prev = sim_dict[i][1]

        alpha_lambda_guess = 




    next_positions = [] #initialize next position array
    

    

        
