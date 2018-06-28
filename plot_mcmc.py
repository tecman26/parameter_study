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
import argparse

run_num = 3
parser = argparse.ArgumentParser(description="Plot run of MCMC")
parser.add_argument('run_num', nargs=1, help="Choose which run to plot", metavar='n' )
args = parser.parse_args()
run_num = int(args.run_num[0])
print(run_num)

trial_pathname = os.path.join(trial_directory,"runs/run_"+str(run_num))
pos_pathname = os.path.join(trial_pathname, "positions.txt")

pos_arr, pos_dict = readPositions(pos_pathname)

pos_arr = np.array(pos_arr)
lambda_vec = pos_arr[:,0]
d_vec = pos_arr[:,1]

def hist2d():
    bin_num = 30
    lambda_data = lambda_vec
    d_data = d_vec

    plt.figure("Color map")
    h, xbins, ybins, img = plt.hist2d(lambda_data, d_data, bins=bin_num, cmap='plasma')
    plt.colorbar()

    plt.figure("Contour plot")
    h,xbins,ybins,img = plt.hist2d(lambda_data, d_data, bins=bin_num,cmap='gray')
    best_vals = np.argwhere(h==h.max())
    lbest = xbins[best_vals[0,0]]
    dbest = ybins[best_vals[0,1]]
    bin_xlen = (xbins[-1]-xbins[0])/len(xbins)
    bin_ylen = (ybins[-1]-ybins[0])/len(ybins)
    print(lbest)
    print(dbest)
    plt.plot(lbest+0.5*bin_xlen,dbest+0.5*bin_ylen,'yD',markersize=8)
    
    # plot contour.  Note that hist2d returns the bin edges so we have to average them to get the center.
    # also, contour() and hist2d() treat the array differently so we need to transpose the cts array.
    CS=plt.contour( 0.5*(xbins[1:]+xbins[:-1]),
                0.5*(ybins[1:]+ybins[1:]),
                h.transpose(), 5, colors=('r','g','b','c','g'),
                linewidths=2)
hist2d()
 

plt.show()
