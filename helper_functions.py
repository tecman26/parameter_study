############################################################################
#
# Stores helping functions for parameter study on mixing length parameter
# and diffusion parameters for matching 1D models to 3D data.
#
############################################################################

import numpy as np
import os
from read3d import *
from read1d import *
import glob

def getLastLine(filename):
    line_list = []
    with open(filename, "r+") as f:
        for line in f:
            #print("line = "+str(line))
            line_list.append(line)
    last_line = line_list[-1]
    #print(last_line)
    job_id = last_line.split()[0]
    return job_id

def getJobID():
    filename = "trial_jobid.txt"
    f = open(filename, "r+")
    job_id = f.readline().rstrip('\n')
    return job_id

def isReady():
    command = "qstat -u f0004519 > q_file.txt"
    os.system(command)
    condition = getLastLine("q_file.txt") == getJobID()

    return condition

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def readOutput(pathname3D):
    # Reads in FLASH output data for 1D or 3D. Pathname should give output
    # directory. Returns one scalar and four 1d numpy arrays.
    
    r_sh = 0
    data_array = []
    

    data_array, r_sh_array = read3d(pathname3D) #read data from output file

    time_array = r_sh_array[:,0]
    time_closest = find_nearest(time_array, 0.135)
    time_closest_val = np.array([x[1] if x[0] == time_closest else 0 for x in r_sh_array])
    #print(time_closest_val[np.flatnonzero(time_closest_val)][0])
    r_sh = time_closest_val[np.nonzero(time_closest_val)][0]

    #----readOutput return format----#
    # Shock radius
    #
    # n x 4 numpy array with columns:
    # # Column 1: radius
    # # Column 2: convective velocity
    # # Column 3: entropy
    # # Column 4: electron fraction
    #--------------------------------#

    r = data_array[0]
    v_con = data_array[1]
    y_e_prof = data_array[2]
    s_prof = data_array[3]

    return (r_sh, r, v_con, y_e_prof, s_prof)

        
    

def readPositions(positions_filename_ref):
    """Function parses positions.txt file and returns dictionary and list giving parameter positions.
       Works for any number of parameters being studied."""
    
    sim_dict = {} #dictionary relating simulation number to parameters
    positions_list = [] #positions from previous trial

    with open(positions_filename_ref, "r") as f:

        for line in f:
            line_list = line.split(", ") #read in line of positions file and split into a list
            sim_num = int(line_list[0]) #simulation number is first entry
            parameters = [float(x) for x in line_list[1:]] #parameters are the rest of line

            positions_list.append(parameters)
            sim_dict[sim_num] = parameters
            
    return positions_list, sim_dict

def writePositions(output_directory, positions_list):
    """Function writes new positions.txt file to 'output_directory'"""
    if os.path.isdir(output_directory) == False:
         os.makedirs(output_directory)
    positions_filename = os.path.join(output_directory,"positions.txt")
    positions_list = list(positions_list)
    with open(positions_filename, "w+") as f:
        num_samples = len(positions_list)
        for i in range(0,num_samples):
            f.write(("%d" % (i+1)).rstrip('\n'))
            parameters = positions_list[i]
            for parameter in parameters:
                f.write((", %f" % parameter).rstrip('\n'))
            f.write('\n')

def chi2(obs, exp, sigma): #Returns chi^2
    chisq = 0
    for i in range(len(obs)):
        if exp[i] != 0:
            chisq += ((obs[i] - exp[i])**2)/sigma[i]
    return chisq/(len(obs))

def l2_norm(obs, exp): #Returns L2 norm instead of chi^2
    norm = 0
    for i in range(len(obs)):
        if exp[i] != 0:
            norm += ((obs[i] - exp[i])**2 / exp[i]**2)
    return norm/(len(obs))

def globfind(run_num): #Find run based on run number 
    data_pathname = glob.glob(os.path.join(trial_directory,"run_mcmcPS_"+str(run_num)))
    data_pathname = data_pathname[0]
    return data_pathname
