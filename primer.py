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
from pyDOE import *
import itertools

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
    num_samples = n_lambda*n_dneut*n_dye*n_deint*n_detrb
    
    
    #----Generate array of evenly spaced sample points----#
    next_positions = []

    #lambda_op = np.linspace(lmin, lmax, n_lambda)
    #dneut_op = dye_op = deint_op = detrb_op = np.linspace(dmin, dmax, n_lambda)
     
    #next_positions = itertools.product(lambda_op, dneut_op, dye_op, deint_op, detrb_op)

    #----Generate sample points based on Latin Hypercube----#
    
    next_positions = lhs(5, samples=num_samples)
    next_positions[:,0] *= (lmax-lmin)
    next_positions[:,0] += lmin
    for i in range(1,5):
        next_positions[:,i] *= (dmax-dmin)
        next_positions[:,i] += dmin

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
