#!/usr/bin/env python

############################################################################
#
# Script Name: read_all_positions.py
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
import ast


trial_pathname = "/mnt/research/SNAPhU/STIR/parameter_study/trial0"
ap_pathname = os.path.join(trial_pathname, "all_positions.txt")

alpha_arr = [] 
# Read in data into 3d numpy array. First index is step number, second is alpha_Lambda or alpha_d,
# third is value for particular walker.
with open(ap_pathname, "r") as ap:
    ap.readline() #Skip header
    for line in ap:
        alphas = []
        alpha_lambdas = []
        alpha_ds = []
        line_lit = ast.literal_eval(line) #Should return tuple of tuples
        for pair in line_lit:
            alpha_lambdas.append(pair[0])
            alpha_ds.append(pair[1])
        alphas = [alpha_lambdas, alpha_ds]
        alpha_arr.append(alphas)
alpha_arr = np.array(alpha_arr)

def plotStep(step_num): #Plot all walkers at a single step of the simulation
    print(alpha_arr[step_num][0])
    print(alpha_arr[step_num][1])
    plt.scatter(alpha_arr[step_num][0], alpha_arr[step_num][1])

plotStep(0)


def hist2d():
    lambda_data = np.ndarray.flatten(alpha_arr[:,0,:])
    d_data = np.ndarray.flatten(alpha_arr[:,1,:])

    plt.hist2d(lambda_data, d_data, bins=20, cmap='plasma')

hist2d()
 

plt.show()
