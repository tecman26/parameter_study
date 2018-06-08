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
        r_sh, data_array = readOutput3D(pathname) #read data from output file
    elif dim == 1:
        r_sh, data_array = readOutput1D(pathname)
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



