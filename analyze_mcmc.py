#!/usr/bin/env python

############################################################################
#
# Script Name: analyze_mcmc.py
# Version 0.0 (June 2018)
# Authors: Theo Cooper and Brandon Barker
#
# Description: Reads in all_positions.txt from trial directory and plots
# positions.
#
############################################################################

import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import *

trial_pathname = "/mnt/research/SNAPhU/STIR/parameter_study/calib1/runs/run_25"
pos_pathname = os.path.join(trial_pathname, "positions.txt")

pos_arr, pos_dict = readPositions(pos_pathname)

pos_arr = np.array(pos_arr)
lambda_vec = pos_arr[:,0]
d_vec = pos_arr[:,1]

def hist2d():
    lambda_data = lambda_vec
    d_data = d_vec

    h, xbins, ybins, img = plt.hist2d(lambda_data, d_data, bins=30, cmap='plasma')
    plt.colorbar()

    best_vals = np.argwhere(h==h.max())
    lbest = xbins[best_vals[0,0]]
    dbest = ybins[best_vals[0,1]]
    plt.plot(lbest,dbest,'kD',markersize=8)

hist2d()
 

plt.show()
