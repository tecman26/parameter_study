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
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from helper_functions import *
import argparse
import pandas as pd
import seaborn as sns

run_num = 3
parser = argparse.ArgumentParser(description="Plot run of MCMC")
parser.add_argument('run_num', nargs=1, help="Choose which run to plot", metavar='n' )
parser.add_argument('--plot', nargs=2, help="Choose dimensions to plot", metavar='p')

# Select the requested run directory
args = parser.parse_args()
run_num = int(args.run_num[0])
trial_pathname = os.path.join(trial_directory,"runs/run_"+str(run_num))
pos_pathname = os.path.join(trial_pathname, "positions.txt")
pos_arr, pos_dict = readPositions(pos_pathname)
pos_arr = np.array(pos_arr)

# Only plot if "--plot" is selected
if args.plot != None:
    d1 = int(args.plot[0])
    d2 = int(args.plot[1])
    vec1 = pos_arr[:,d1]
    vec2 = pos_arr[:,d2]


bin_num = 30
H, edges = np.histogramdd(pos_arr, bins=(bin_num, bin_num, bin_num, bin_num, bin_num), \
                   range=((lmin,lmax),(dmin,dmax),(dmin,dmax),(dmin,dmax),(dmin,dmax)))

H = np.array(H)
#print(H)
full_bestvals = np.argwhere(H==np.max(H))[0]
l_bin_len = (lmax-lmin)/bin_num
d_bin_len = (dmax-dmin)/bin_num
#print(full_bestvals)
best_pos = [edges[i][full_bestvals[i]] for i in range(5)]
best_pos +=  np.array([0.5*l_bin_len,0.5*d_bin_len, 0.5*d_bin_len,0.5*d_bin_len, 0.5*d_bin_len])

print("Best position: "+str(best_pos))

f = lambda x: np.exp(-(x))

def hist2d():
    data1 = vec1
    data2 = vec2

    plt.figure("Color map")
    h, xbins, ybins, img = plt.hist2d(data1, data2, bins=bin_num, cmap='plasma', norm=colors.LogNorm())
    plt.colorbar()
    plt.xlabel("Parameter 1")
    plt.ylabel("Parameter 2")

    plt.figure("Contour plot")
    h,xbins,ybins,img = plt.hist2d(data1, data2, bins=bin_num,cmap='gray', norm=colors.LogNorm())
    best_vals = np.argwhere(h==h.max())
    bin_xlen = (xbins[-1]-xbins[0])/len(xbins)
    bin_ylen = (ybins[-1]-ybins[0])/len(ybins)
    best1 = xbins[best_vals[0,0]]+0.5*bin_xlen
    best2 = ybins[best_vals[0,1]]+0.5*bin_ylen
    print(best1)
    print(best2)
    plt.plot(best1,best2,'yD',markersize=8)
    plt.xlabel("Parameter 1")
    plt.ylabel("Parameter 2")
    
    # plot contour.  Note that hist2d returns the bin edges so we have to average them to get the center.
    # also, contour() and hist2d() treat the array differently so we need to transpose the cts array.
    CS=plt.contour( 0.5*(xbins[1:]+xbins[:-1]),
                0.5*(ybins[1:]+ybins[1:]),
                h.transpose(), 5, cmap='plasma',
                norm=colors.LogNorm(), linewidths=2)

def pairmap():
    hmax = np.max(H)
    level_list = [0.5*hmax*f(x) for x in reversed(range(1,6))]
    print(level_list)

    pos_df = pd.DataFrame(pos_arr, columns=['alpha_Lambda', 'alpha_Dneut', 'alpha_Dye', 'alpha_Deint', 'alpha_Detrb'])
    #sns.pairplot(pos_df)
    g = sns.PairGrid(pos_df)
    #g.map_upper(plt.scatter)
    g.map_diag(plt.hist, log=True)
    g.map_lower(sns.kdeplot, n_levels=5, locator=matplotlib.ticker.LinearLocator(), cmap='plasma')
    #sns.kdeplot(pos_df['alpha_Detrb'], pos_df['alpha_Dneut'], n_levels=5, levels=level_list, cmap='plasma')
    #sns.kdeplot(pos_df['alpha_Detrb'], pos_df['alpha_Dneut'], n_levels=5, locator=matplotlib.ticker.LinearLocator(), cmap='plasma')


if args.plot != None:
    hist2d()

    #pairmap()
    plt.show()
