#!/usr/bin/env python

############################################################################
#
# Script Name: markov.py
# Version 0.0 (June 2018)
# Authors: Theo Cooper and Brandon Barker
#
# Description: For use in parameter studies for the mixing length parameter
# and diffusion parameters for matching 1D models to 3D data.
#
############################################################################

from scipy.stats import chisquare
import numpy as np
import sys, os
import glob
from helper_functions import *
from ps_setup import *
from ps_runjob import *
import time
from settings import *
from emulators.py import *


# This "gets" the program name and assigns it to a variable.
ScriptName = os.path.split(sys.argv[0])[1].split('.')[0]

chi2_mod = lambda obs_array, exp_array: chisquare(obs_array, exp_array)[0] # returns chi2 without p-value


if __name__ == '__main__':
    # Put initialization stuff here. Define timestep etc etc etc

    # This prints the program name. Not necessary, put nice to do
    # before other output. Stylish.

    print('\n************************************')
    print('**          %s ' % ScriptName )
    print('************************************\n')

    
    #----Read in 3D simulation data for comparison----#
    

    r_sh_3D, r_3D, v_con_3D, y_e_3D, s_3D = readOutput(data_dir3D, 3)


    #----specify which walker step is being run----#
    
    #step_num = input("Enter step number ")

    runs_directory = os.path.join(trial_directory,"runs")
    if os.path.isdir(runs_directory) == False:
        os.makedirs(runs_directory)
    run_num = 1
    last_run = glob.glob(os.path.join(runs_directory,"run*"))
    if len(last_run) == 0:
        pass
    else:
        last_run = last_run[-1]
        run_num = last_run.split("_")
        run_num = run_num[-1]
        run_num += 1
    output_directory = os.path.join(trial_directory,"runs/run_"+str(run_num))

    input_directory = trial_directory
    
    positions_filename_ref = input_directory+"/positions.txt"
    

        
    #----Read in previous simulation data----#

    # --------------------------------------------------------------------------------------
    #  positions.txt format:
    #  1, alpha_lambda_1, alpha_d_1
    #  2, alpha_lambda_2, alpha_d_2
    #  ... 
    #  i, alpha_lambda_i, alpha_d_i
    #
    #  for num_walkers lines
    # --------------------------------------------------------------------------------------
    # integrated_data_i.txt format:
    # r (km), v_con (km/s), y_e_prof_prev, s_prof_prev
    # --------------------------------------------------------------------------------------

    #----Loop for running MCMC----#
    #'alpha' is left out of variable names to save space
    
    lambda_start = (lmax-lmin)*np.random.random_sample() + lmin
    d_start = (dmax-dmin)*np.random.random_sample() + dmin
    
    pos_list = [[lambda_start, d_start]] # Position guess list

    lambda_prev = lambda_start
    d_prev = d_start
    
    lambda_step = 0.05
    d_step = 0.05
    
    for i in range(nSteps):

        #----Generate guesses----#
        
        lambda_guess = 0
        d_guess = 0
        
        lambda_ok = False
        while lambda_ok == False:
            lambda_guess = lambda_prev + 2*lambda_step*np.random.random_sample() - lambda_step
            if lambda_guess > lmin and lambda_guess < lmax:
                lambda_ok = True
       
        d_ok = False
        while d_ok == False:
            d_guess = d_prev + 2*d_step*np.random.random_sample() - d_step
            if d_guess > dmin and d_guess < dmax:
                d_ok = True

    
        
        #----Compare results from emulator map----#

        param_prev = [lambda_prev, lambda_guess]
        param_guess = [lambda_guess, d_guess]

        r_sh_p, r_sh_p_std = emulRshock(param_prev)
        v_con_p, v_con_p_std = emulVcon(param_prev)
        y_e_p, y_e_p_std = emulYE(param_prev)
        s_p, s_p_std = emulS(param_prev)
        
        r_sh_g, r_sh_g_std = emulRshock(param_guess)
        v_con_g, v_con_g_std = emulVcon(param_guess)
        y_e_g, y_e_g_std = emulYE(param_guess)
        s_g, s_g_std = emulS(param_guess)


        #----Metropolis-Hastings Algorithm----#


        # These chi2 terms can be weighted later
        chi2_p = chi2_mod(r_sh_p, r_sh_3D) + chi2_mod(v_con_p, v_con_3D) + chi2_mod(y_e_p, y_e_3D) + chi2_mod(s_p, s_3D)
        chi2_g = chi2_mod(r_sh_g, r_sh_3D) + chi2_mod(v_con_g, v_con_3D) + chi2_mod(y_e_g, y_e_3D) + chi2_mod(s_g, s_3D)

        # Likelihood ratio of both sets of data (also known as acceptance probability)
        p_acc = np.exp(-chi2_g + chi2_p)

        p_thresh = np.random.random_sample() # threshold probability, chosen randomly between 0 and 1

        if p_acc < p_thresh: # if acceptance probability doesn't exceed threshold

            pos_list.append(pos_prev_dict[i])
            
        else: # if acceptance probability exceeds the threshold

            pos_list.append(pos_g_dict[i])

            with open(os.path.join(output_directory,"ch_sq.txt"), "a+") as chi_file:
                chi_file.write(str(pos_g_dict[i][0])+","+str(pos_g_dict[i][1])+","+str(chi2_g))

