# Functions for calibrating and 
# returning emulators
# 
#----------------------------------


import numpy as np
from sklearn import gaussian_process
from helper_functions import *
from read1d import *
import glob
import pickle

#initialize emulators
kernel_choice = gaussian_process.kernels.RBF(0.05)
r_sh_file = "r_sh_emul_storage.pkl"
v_con_file = "v_con_emul_storage.pkl"
y_e_file = "y_e_emul_storage.pkl"
s_file = "s_emul_storage.pkl"

r_sh_emul = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
v_con_emul = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
y_e_emul = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
s_emul = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)

def calibrateEmulators(data_dir): #positions file should have same format as positions.txt
    #data directory contains all run directories from calibration run
    pos_pathname = os.path.join(data_dir, "positions.txt")
    pos_dict, pos_arr = readPositions(pos_pathname)
    pos_arr = np.array(pos_arr)
    num_samples = pos_arr.shape[0]
    
    #list of radius values, for reference
    radius_ref = []
    #shock radius column vector
    r_sh_arr = []
    #2d arrays containing v_con vectors
    v_con_arr = []
    y_e_arr = []
    s_arr = []
    
    for i in range(1,num_samples+1):
        data_pathname = glob.glob(os.path.join(data_dir,"run_mcmcPS_"+str(i)+"*"))
        data_pathname = data_pathname[0]
        
        r, v_con, y_e_prof, s_prof, r_sh = read1d(data_pathname)
        
        if i == 1:
            radius_ref = r
        
        r_sh_arr.append(r_sh)
        v_con_arr.append(v_con)
        y_e_arr.append(y_e_prof)
        s_arr.append(s_prof)
    
    r_sh_arr = np.transpose(np.array(r_sh_arr))
    v_con_arr = np.array(v_con_arr)
    y_e_arr = np.array(y_e_arr)
    s_arr = np.array(s_arr)
    
    r_sh_emul.fit(pos_arr,r_sh_emul)
    v_con_emul.fit(pos_arr,v_con_arr)
    y_e_emul.fit(pos_arr,y_e_arr)
    s_emul.fit(pos_arr,s_emul)

def storeEmulators(file1=r_sh_file, file2=v_con_file, file3=y_e_file, file4=s_emul_file):
    with open(file1, "w+b") as f1:
        pickle.dump(r_sh_emul, f1, pickle.HIGHEST_PROTOCOL)
    with open(file2, "w+b") as f2: 
        pickle.dump(v_con_emul, f2, pickle.HIGHEST_PROTOCOL)
    with open(file3, "w+b") as f3: 
        pickle.dump(y_e_emul, f2, pickle.HIGHEST_PROTOCOL)
    with open(file2, "w+b") as f4: 
        pickle.dump(s_emul, f4, pickle.HIGHEST_PROTOCOL)
    
def loadEmulators(file1=r_sh_file, file2=v_con_file, file3=y_e_file, file4=s_emul_file):
    r_sh_load = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
    v_con_load = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
    y_e_load = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
    s_load = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)


    with open(file1, "r+b") as f1:
        r_sh_load = pickle.load(f1)
    with open(file2, "r+b") as f2: 
        v_con_load = pickle.load(f2)
    with open(file3, "r+b") as f3: 
        y_e_load = pickle.load(f3)
    with open(file2, "r+b") as f4: 
        s_load = pickle.load(f4)
 
    return r_sh_load, v_con_load, y_e_load, s_load

def radii():
    return radius_ref
    
def emulRShock(arr): #Should be fed one set of n parameters or n arrays of parameters
    return r_sh_emul.predict(arr,return_std=True)

def emulVCon(arr):
    return v_con_emul.predict(arr,return_std=True)

def emulYE(arr):
    return y_e_emul.predict(arr,return_std=True)

def emulS(arr):
    return s_emul.predict(arr,return_std=True)


calibrateEmulators(trial_directory)
storeEmulators()
