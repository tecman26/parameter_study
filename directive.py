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

# import yt?
# from optparse import OptionParser # For if we need commad line arguments

# This "gets" the program name and assigns it to a variable.
ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]

if __name__ == '__main__':
    
    first_sim = True
    filename = "none"
    
    parser = OptionParser()
    parser.add_option("-r", "--read_file", action="store", dest="filename", help="Submit data file from previous simulation to set initial walker positions")
    
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
    
    num_walkers = 1
    
    start_positions = []
    
    if first_sim == True:
        #----Read in single-parameter alpha_lambda study----#

        # v_con_sing = 
        # r_sh_sing = 
        # y_e_prof_sing = 
        # s_prof_sing =
    
        lambda_min = 0
        lambda_max = 2 # We can narrow these down once we have data from the previous alpha_lambda parameter study
        
        #----Generate array of random starting points--#
        alpha_lambda_range = range(lambda_min,lambda_max) 
        alpha_d_range = range(0,1)
        
        
    
     else:
        #----Read in previous simulation data----#


        # v_con_prev = 
        # r_sh_prev = 
        # y_e_prof_prev = 
        # s_prof_prev =

    
    
