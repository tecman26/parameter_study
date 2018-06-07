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
#import readData1D
#import ps_setup

# import yt?
# from optparse import OptionParser # For if we need commad line arguments

# This "gets" the program name and assigns it to a variable.
ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]

if __name__ == '__main__':
    
    first_sim = True
    dirname = "none"
    
    parser = OptionParser()
    parser.add_option("-r", "--read_dir", action="store", dest="dirname", help="Submit directory from previous batch of simulations")
    
    positions_filename_ref = dirname+"/positions.txt"
    
    if dirname != "none":
        first_sim = False
    elif os.path.isdir(dirname) == False:
        print("Please enter the name of a directory")
        return
    elif os.path.isfile(positions_filename_ref) == False:
        print("No 'positions.txt' file found")
        return
    
    output_directory = "~/BANG/parameter_study/trial0/step1/"

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
        #  1, alpha_lambda_1, alpha_d_1
        #  2, alpha_lambda_2, alpha_d_3
        #  ... 
        #  i, alpha_lambda_i, alpha_d_i
        #  
        #  for num_walkers lines
        # --------------------------------------------------------------------------------------
        # integrated_data_i.txt format:
        # r (km), v_con (km/s), y_e_prof_prev, s_prof_prev
        # --------------------------------------------------------------------------------------

        positions_ref = [] #reference positions from previous trial
        sim_dict = {} #dictionary relating simulation number to parameters

        with open(positions_filename_ref) as f:
            
            for i in range(num_walkers):
                
                line_list = f.readline().split(", ") #read in line of positions file and split into a list
                sim_num = line_list[0] #simulation number is first entry
                parameters = line_list[1:] #parameters are the rest of line
                
                positions_ref.append(parameters)
                sim_dict[sim_num] = parameters
            
        for i in range(1,num_walkers):
            data_pathname = str(glob.glob(dirname+"/run_mcmcPS_"+str(i)+"*")) #glob function returns a list that should have only one file (the one with sim_num = i)
            readData1D.readData1D(data_pathname+"/output") #read data from output file
            
 

            # v_con_prev = 
            # r_sh_prev = 
            # y_e_prof_prev = 
            # s_prof_prev =
            
            
    
    
    #----Output positions file----#
    
    positions_filename_out = output_directory+"positions.txt"
    with open(positions_filename_out) as f:
        for i in range(num_walkers):
            for parameter in next_positions[i]:
                f.write(("%f, " % parameter).rstrip('\n'))
                f.write('\n')
    
    #----Set up next simulation----#
    
    #for i in range(num_walkers):
        #runsetup.[function to be named](alpha_lambda=next_positions[i][0], alpha_dnext_positions[i][1],
        # pathname=output_directory)
        
        
