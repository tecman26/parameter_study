#!/usr/bin/env python

############################################################################
#
# Script Name: primer.py
# Version 0.0 (June 2018)
# Authors: Theo Cooper and Brandon Barker
#
# Description: For use in parameter studies for the mixing length parameter
# and diffusion parameters for matching 1D models to 3D data. Generates
# intitial set of num_samples simulations and primes simulation files.
#
############################################################################

import numpy as np
import sys, os
from optparse import OptionParser
import glob
from helper_functions import *
from ps_setup import *
from ps_runjob import *
from settings import *
import time
from pyDOE import *

# This "gets" the program name and assigns it to a variable.
ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]

if __name__ == '__main__':

    # This prints the program name. Not necessary, put nice to do
    # before other output. Stylish.

    print('\n************************************')
    print('**          %s ' % ScriptName )
    print('************************************\n')

    output_directory = trial_directory
    
#----Hard-coded results from single-parameter alpha_lambda study----#
    
    #IMPORTANT PARAMETER: this determines how many sample points to set up
    num_samples = 512
    
    
    #----Generate array of random starting points using latin hypercube sampling----#
    
    
    next_positions = lhs(2,num_samples) 

    #----Output positions file----#
    
    
    writePositions(output_directory, next_positions)
    
            
            
    #----Set up and run next simulation batch----#
    
    setup(output_directory)
    runjob(output_directory) 

    #interval = 300 #seconds to sleep between checking    
    #ready = False

    #while ready == False:
        #print("Not ready")
    #    time.sleep(interval)
    #    ready = isReady()   
