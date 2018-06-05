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
# import yt?
# from optparse import OptionParser # For if we need commad line arguments

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

    # import [plotting script file]
    # read in 3D data into arrays using imported software
    # v_con_3D = 
    # r_sh_3D = 
    # y_e_prof_3D = 
    # s_prof_3D = 

    #----Read in previous 1D simulation data----#

    # read in data from mixing-length parameter study for calibrating starting points into arrays
    # v_con_prev = 
    # r_sh_prev = 
    # y_e_prof_prev = 
    # s_prof_prev =
    
    
    
