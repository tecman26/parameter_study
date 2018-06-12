############################################################################
#
# Stores helping functions for parameter study on mixing length parameter
# and diffusion parameters for matching 1D models to 3D data.
#
############################################################################

import numpy as np
import os
from read3D import *
from read1D import *

def readOutput(pathname, dim):
    # Reads in FLASH output data for 1D or 3D. Pathname should give output
    # directory. Returns one scalar and four 1d numpy arrays.
    
    r_sh = 0
    data_array = []
    
    if dim == 3:
        data_array, r_sh = read3d(pathname) #read data from output file
    elif dim == 1:
        data_array, r_sh = read1d(pathname)
    else:
        print("Enter either '1' or '3' for number of dimensions")
    
    #----readOutput return format----#
    # Shock radius
    #
    # n x 4 numpy array with columns:
    # # Column 1: radius
    # # Column 2: convective velocity
    # # Column 3: entropy
    # # Column 4: electron fraction
    #--------------------------------#
    
    r = data_array[:,0]
    v_con = data_array[:,1]
    y_e_prof = data_array[:,2]
    s_prof = data_array[:,3]
    
    return (r_sh, r, v_con, y_e_prof, s_prof)

def readPositions(positions_filename_ref):
    """Function parses positions.txt file and returns dictionary and list giving parameter positions.
       Works for any number of parameters being studied."""
    
    sim_dict = {} #dictionary relating simulation number to parameters
    positions_list = [] #positions from previous trial

    with open(positions_filename_ref) as f:

        for i in range(1,num_walkers+1):

            line_list = f.readline().split(", ") #read in line of positions file and split into a list
            sim_num = line_list[0] #simulation number is first entry
            parameters = line_list[1:] #parameters are the rest of line

            positions_list.append(parameters)
            sim_dict[sim_num] = parameters
            
    return sim_dict, positions_list

def writePositions(output_directory, positions_list):
    """Function writes new positions.txt file to 'output_directory'"""
    positions_filename = os.path.join(output_directory,"positions.txt")
    with open(positions_filename, "w+") as f:
        num_walkers = len(positions_list)
        for i in range(0,num_walkers):
            f.write(("%d" % (i+1)).rstrip('\n'))
            parameters = positions_list[i]
            for parameter in parameters:
                f.write((", %f" % parameter).rstrip('\n'))
            f.write('\n')
