#!/usr/bin/env python

############################################################################
#
# Script Name: directive.py
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
from argparse import ArgumentParser
import glob
from helper_functions import *
from ps_setup import *
from ps_runjob import *
import time
from settings import *



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


    step_num = 1
    parser = ArgumentParser()
    parser.add_argument("s", default=1, help="step number of simulation", type=int)
    args = parser.parse_args()
    step_num = args.s 
    output_directory = os.path.join(trial_directory,"step"+str(step_num))
    if os.path.isdir(output_directory) == True:
        print("Warning: step directory already exists")
    else:
        os.mkdir(output_directory)

    input_directory = os.path.join(trial_directory,"step"+str(int(step_num)-1))
    
    positions_filename_ref = input_directory+"/positions.txt"
    
    if  os.path.isdir(input_directory) == False:
        print("Please enter a valid step number")
        sys.exit()
    elif os.path.isfile(positions_filename_ref) == False:
        print("No 'positions.txt' file found")
        sys.exit()
    

        
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

    # Fill a dictionary and a list with the sets of parameters output by the previous sim
    pos_prev_dict, pos_prev_list = readPositions(positions_filename_ref)
    
    #print(pos_prev_dict)

    num_walkers = len(pos_prev_list) #number of Markov chain walkers
    num_parameters = len(pos_prev_list[0]) #number of parameters being varied
    
    #print(num_walkers)    
    #dictionary relating simulation number to positions and list containing tuples of positions

    
    #----Loop for generating guess positions----#
    
    pos_g_list = [] # Position guess list
    pos_g_dict = {} # Position guess dict
    
    for i in range(1,num_walkers+1):
        #In this loop, 'alpha' is left out of variable names to save space
        
        lambda_step = 0.05
        d_step = 0.05
        
        #Pull previous parameter positions
        #print(pos_prev_dict[i])
        lambda_prev = pos_prev_dict[i][0]
        d_prev = pos_prev_dict[i][1]

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

        pos_g_list.append([lambda_guess, d_guess])
        pos_g_dict[i] = [lambda_guess, d_guess]
    
    #----Write guess positions to file----#
    #print("pos_prev_list = "+str(pos_prev_list))
    #print("pos_prev_list = "+str(pos_g_list))
    
    writePositions(output_directory, pos_g_list) #See helper_functions.py for documentations
    
    #----Set up and run batch of guess simulations----#
    
    # command = "./ps_setup.py"
    # print(command)
    # os.system(command)
    setup(output_directory) #run the "setup" function from the ps_setup.py script
    
    runjob(output_directory)
    
    interval = 300 #seconds to sleep between checking
    ready = False
    
    while ready == False:
        #print("Not ready")
        time.sleep(interval)
        ready = isReady()
        
    #----Read and compare results of simulations----#

    final_positions = []

    for i in range(1,num_walkers+1):

        # glob function returns a list that should have only one file (the one with sim_num = i)
        prev_data_pathname = glob.glob(os.path.join(input_directory,"run_mcmcPS_"+str(i)+"*"))
        print("prev_data_pathname = "+str(prev_data_pathname))
        prev_data_pathname = prev_data_pathname[0]

        guess_data_pathname = glob.glob(os.path.join(output_directory,"run_mcmcPS_"+str(i)+"*"))
        guess_data_pathname = guess_data_pathname[0]


        r_sh_p, r_p, v_con_p, y_e_p, s_p = readOutput(data_dir3D, 1, prev_data_pathname, step_num-1)
        r_sh_g, r_g, v_con_g, y_e_g, s_g = readOutput(data_dir3D, 1, guess_data_pathname, step_num)

        if r_sh_p == 0 or r_p == 0 or v_con_p == 0 or y_e_p == 0 or s_p == 0:

            final_positions.append(pos_prev_dict[i])
            try:
                with open(os.path.join(output_directory,"ch_sq.txt"), "a+") as chi_file:
                    chi_file.write(str(pos_prev_dict[i][0])+","+str(pos_prev_dict[i][1])+",0")
            except:
                pass

            os.system("rm -r "+guess_data_pathname)
            os.system("cp -r "+prev_data_pathname+" "+output_directory)
            
            continue
        if r_sh_g == 0 or r_g == 0 or v_con_g == 0 or y_e_g == 0 or s_g == 0:
            final_positions.append(pos_prev_dict[i])
            try:
                with open(os.path.join(output_directory,"ch_sq.txt"), "a+") as chi_file:
                    chi_file.write(str(pos_prev_dict[i][0])+","+str(pos_prev_dict[i][1])+",0")
            except:
                pass



            os.system("rm -r "+guess_data_pathname)
            os.system("cp -r "+prev_data_pathname+" "+output_directory)

            continue
        #----Metropolis-Hastings Algorithm----#


        # These chi2 terms can be weighted later
        chi2_p = chi2_mod(r_sh_p, r_sh_3D) + chi2_mod(v_con_p, v_con_3D) + chi2_mod(y_e_p, y_e_3D) + chi2_mod(s_p, s_3D)
        chi2_g = chi2_mod(r_sh_g, r_sh_3D) + chi2_mod(v_con_g, v_con_3D) + chi2_mod(y_e_g, y_e_3D) + chi2_mod(s_g, s_3D)

        # Likelihood ratio of both sets of data (also known as acceptance probability)
        p_acc = np.exp(-chi2_g + chi2_p)

        p_thresh = np.random.random_sample() # threshold probability, chosen randomly between 0 and 1

        if p_acc < p_thresh: # if acceptance probability doesn't exceed threshold

            final_positions.append(pos_prev_dict[i])
            try:
                with open(os.path.join(output_directory,"ch_sq.txt"), "a+") as chi_file:
                    chi_file.write(str(pos_prev_dict[i][0])+","+str(pos_prev_dict[i][1])+","+str(chi2_p))


            # Remove the guess data files from directory and replace with previous data, for use in
            # next step.
            os.system("rm -r "+guess_data_pathname)
            os.system("cp -r "+prev_data_pathname+" "+output_directory)
            
        else: # if acceptance probability exceeds the threshold

            final_positions.append(pos_g_dict[i])
            try:
                with open(os.path.join(output_directory,"ch_sq.txt"), "a+") as chi_file:
                    chi_file.write(str(pos_g_dict[i][0])+","+str(pos_g_dict[i][1])+","+str(chi2_g))

    #----Write new positions file----#
    
    writePositions(final_positions, output_directory)
    
    #----Append new positions to all_positions file---#

    positions_filename_out = os.path.join(trial_directory,"all_positions.txt")
    with open(positions_filename_out, "w+") as f:
        for i in range(num_walkers-1):
            parameters = next_positions[i]
            f.write(("(").rstrip('\n'))
            f.write(str(parameters[0]).rstrip('\n'))
            for parameter in parameters[1:]:
                f.write((", %f" % parameter).rstrip('\n'))
            f.write(("), ").rstrip('\n'))
        parameters = next_positions[num_walkers-1]
        f.write(("(").rstrip('\n'))
        f.write(str(parameters[0]).rstrip('\n'))
        for parameter in parameters[1:]:
            f.write((", %f" % parameter).rstrip('\n'))
        f.write(")\n")
               
