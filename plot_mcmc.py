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
import matplotlib
from helper_functions import *
import argparse

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)

run_num = 3
parser = argparse.ArgumentParser(description="Plot run of MCMC")
parser.add_argument('run_num', nargs=1, help="Choose which run to plot", metavar='n' )
args = parser.parse_args()
run_num = int(args.run_num[0])

trial_pathname = os.path.join(trial_directory,"runs/run_"+str(run_num))
#trial_pathname = "test_dir"
pos_pathname = os.path.join(trial_pathname, "positions.txt")

pos_arr, pos_dict = readPositions(pos_pathname)

pos_arr = np.array(pos_arr)

lambda_vec = pos_arr[:,0]
d_vec = pos_arr[:,1]

print(len(lambda_vec))

corr = np.corrcoef(np.transpose(pos_arr))
print("Correlation matrix:")
print(corr)

w, v = np.linalg.eig(corr)
v_mod = v
v_mod[:,0] = np.sqrt(w[0])*v_mod[:,0]
v_mod[:,1] = np.sqrt(w[1])*v_mod[:,1]

def hist2d():
    bin_num = 30
    lambda_data = lambda_vec
    d_data = d_vec

    plt.figure("Color map")
    h, xbins, ybins, img = plt.hist2d(lambda_data, d_data, bins=bin_num, cmap='plasma')
    bar = plt.colorbar()
    bar.set_label("Number of steps")
    plt.suptitle("2D histogram of Markov chain positions", fontsize=20)
    #plt.title("(1 walker, 10^6 steps)")
    plt.xlabel("alpha_Lambda")
    plt.ylabel("alpha_D")

    plt.figure("Contour plot")
    h,xbins,ybins,img = plt.hist2d(lambda_data, d_data, bins=bin_num,cmap='gray_r')
    best_vals = np.argwhere(h==h.max())
    bin_xlen = (xbins[-1]-xbins[0])/len(xbins)
    bin_ylen = (ybins[-1]-ybins[0])/len(ybins)
    lbest = xbins[best_vals[0,0]]+0.5*bin_xlen
    dbest = ybins[best_vals[0,1]]+0.5*bin_ylen
    print("Best alpha_Lambda = "+str(lbest))
    print("Best alpha_D = "+str(dbest))
    cmap_choice = matplotlib.cm.get_cmap('plasma')
    plt.plot(lbest,dbest,'D',markersize=8, color=cmap_choice(0.99))
    plt.xlabel("alpha_Lambda")
    plt.ylabel("alpha_D")
    
    # plot contour.  Note that hist2d returns the bin edges so we have to average them to get the center.
    # also, contour() and hist2d() treat the array differently so we need to transpose the cts array.
    f = lambda x: np.exp(-(x/3)**2/2) # x = number of standard deviations away, assuming Gaussiang distribution
    contour_levels = list(reversed([h.max()*f(x) for x in range(1,6)])) 
    #color_set = matplotlib.colors.LogNorm(contour_levels)
    CS=plt.contour( 0.5*(xbins[1:]+xbins[:-1]),
                0.5*(ybins[1:]+ybins[1:]),
                h.transpose(), 5, levels=contour_levels,  cmap=cmap_choice,
                norm=matplotlib.colors.Normalize(vmin=1, vmax=h.max()), linewidths=2)
    plt.suptitle("Contour plot of best Markov chain positions", fontsize=20)
    plt.quiver(lbest, dbest, v_mod[0,0], v_mod[1,0], scale=1.5, scale_units = 'inches',
                color='r', label='least correlation')
    plt.quiver(lbest, dbest, v_mod[0,1], v_mod[1,1], scale=1.5, scale_units = 'inches',
                color='c', label='most correlation')
    plt.legend(fontsize='14')

hist2d()
 

plt.show()
