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
#import runsetup

# import yt?
# from optparse import OptionParser # For if we need commad line arguments

# This "gets" the program name and assigns it to a variable.
ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]

if __name__ == '__main__':
    
    first_sim = True
    filename = "none"
    
    parser = OptionParser()
    parser.add_option("-r", "--read_file", action="store", dest="filename", help="Submit data file from previous simulation to set initial walker positions")
    
    output_directory = "~/BANG/parameter_study/trial0/step1/"
    
    if filename != "none":
        first_sim = False
    elif os.path.isfile(filename) == False:
        print("File does not exist.")
        return

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
    threeD_File = "%smesa20_v_LR.dat" % dataDir
    data = np.genfromtxt(threeD_File)

    mean_shock_radius = data[:,11]


    # import [plotting script file]
    # read in 3D data into arrays using imported software
    # v_con_3D = 
    # r_sh_3D = 
    # y_e_prof_3D = 
    # s_prof_3D = 

    # --------------------------------------------------------------------------------------
    #  Depending on how this should be done, we may need a large outer loop
    #  that loops of various values of the parameters, runs the appropriate simulation,
    #  and goes on. 
    # --------------------------------------------------------------------------------------
    
    num_walkers = 1 #number of Markov chain walkers
    num_parameters = 2 #number of parameters being varied
    
    start_positions = [] #initialize starting position array
    next_positions = [] #initialize next position array
    
    if first_sim == True:
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
    
     else:
        
        
        #----Read in previous simulation data----#
         
        # --------------------------------------------------------------------------------------
        #  positions.txt format:
        #  0, alpha_lambda_0, alpha_d_0
        #  1, alpha_lambda_1, alpha_d_1
        #  ... 
        #  i, alpha_lambda_i, alpha_d_i
        #  
        #  for num_walkers lines
        # --------------------------------------------------------------------------------------
        # integrated_data_i.txt format:
        # r (km), v_con (km/s), 
        # y_e_prof_prev = 
        # s_prof_prev =
        #  ... for num_walkers lines
        # --------------------------------------------------------------------------------------

        positions_prev = []
        with open(filename) as positions:
            
            for i in range(num_walkers):
                for 
                positions.read(
 
            # v_con_prev = 
            # r_sh_prev = 
            # y_e_prof_prev = 
            # s_prof_prev =
            
            
    
    
    #----Output positions file----#
    
    positions_filename = output_directory+"positions.txt"
    with open(positions_filename) as file:
        for i in range(num_walkers):
            for parameter in next_positions[i]:
                file.write(("%f, " % parameter).rstrip('\n'))
                file.write('\n')
    
    #----Set up next simulation----#
    
    for i in range(num_walkers):
        #runsetup.[function to be named](alpha_lambda=next_positions[i][0], alpha_dnext_positions[i][1],
        # pathname=output_directory)
        
        
