############################################################################
#
# Stores helping functions for parameter study on mixing length parameter
# and diffusion parameters for matching 1D models to 3D data.
#
############################################################################

import numpy as np
import os
from read3d import *
from settings import *
#from read1D import *

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

        for i in range(num_walkers):

            line_list = f.readline().split(", ") #read in line of positions file and split into a list
            sim_num = line_list[0] #simulation number is first entry
            parameters = line_list[1:] #parameters are the rest of line

            positions_list.append(parameters)
            sim_dict[sim_num] = parameters

    return sim_dict, positions_list

def getOldAlphas(file):
    """
    Given filename path for positions_old.txt, reads it and
    fills in the values.
    """

    param = np.loadtxt(file)
    alphaL = param[:,0]
    alphaD = param[:,1]

    return alphaL, alphaD

def writeParameters(alpha_l_options, alpha_d_options):

    num_alpha_l = 32
    num_alpha_d = 16

    dataDir = "./data"
    pathBase = "mcmc_step" + str(mcmc_step)
    pos_filename = os.path.join(pathBase, "positions.txt") # cumulative list of pairs
    pos_old_filename = os.path.join(pathBase, "positions_old.txt")
    pos_filename_cp = os.path.join(pathBase, "positions_cp.txt")

    if os.path.isfile(pos_filename_cp):
        os.remove(pos_filename_cp)

    next_positions = []

    # This bit will create the cumulative paramaters list.
    with open(pos_filename, "w+") as f:
        f.write("#alpha_l  alpha_d\n")

    with open(pos_old_filename, "w+") as f:
        f.write("#alpha_l  alpha_d\n")

    for i in range(num_alpha_l):
        for j in range(num_alpha_d):
            alpha_l = alpha_l_options[i]
            alpha_d = alpha_d_options[j]
            next_positions.append([alpha_l, alpha_d])

            # ----------------------------------------------------------
            #  Writes to positions.txt. Contains cumulative list of
            #  ordered pairs.
            # ----------------------------------------------------------
            with open(pos_filename, "a+") as f:
                f.write(("%f %f" % (alpha_l,alpha_d) ).rstrip('\n'))
                f.write('\n')

            # ----------------------------------------------------------
            #  BAD. Writes to positions_cp.txt. Contains cumulative list of
            #  ordered pairs. ONLY for use in ps_setup. Fix later.
            # ----------------------------------------------------------
            with open(pos_filename_cp, "a+") as f:
                f.write(("%f %f" % (alpha_l,alpha_d) ).rstrip('\n'))
                f.write('\n')


        # --------------------------------------------------------------
        # Writes positions_old.txt. contains only the values of alphas.
        # Does not contain the list of ordered pairs.
        # --------------------------------------------------------------
        with open(pos_old_filename, "a+") as f:
            if( i < num_alpha_d ):
                f.write(("%f %f" % (alpha_l,alpha_d_options[i]) ).rstrip('\n'))
                f.write('\n')
            else:
                f.write(("%f 0" % (alpha_l) ).rstrip('\n'))
                f.write('\n')



    return 0
