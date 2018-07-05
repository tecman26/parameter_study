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
from settings import *

def resh(arr):
    return np.reshape(arr,(1,-1))

#initialize emulators
kernel_choice = gaussian_process.kernels.RBF(0.05)
r_sh_file = os.path.join(trial_directory,"r_sh_emul_storage.pkl")
v_con_file = os.path.join(trial_directory,"v_con_emul_storage.pkl")
y_e_file = os.path.join(trial_directory,"y_e_emul_storage.pkl")
s_file = os.path.join(trial_directory,"s_emul_storage.pkl")

r_sh_emul = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
v_con_emul = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
y_e_emul = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
s_emul = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
#list of radius values, for reference
radius_ref = []

def calibrateEmulators(data_dir): #positions file should have same format as positions.txt
    #data directory contains all run directories from calibration run
    pos_pathname = os.path.join(data_dir, "positions.txt")
    pos_arr, pos_dict = readPositions(pos_pathname)
    pos_arr = np.array(pos_arr)
    num_samples = pos_arr.shape[0]

    #shock radius column vector
    r_sh_arr = []
    #2d arrays containing v_con vectors
    v_con_arr = []
    y_e_arr = []
    s_arr = []
    
    bad_runs_file = os.path.join(trial_directory, "bad_runs.txt")
    if os.path.isfile(bad_runs_file) == True:
        os.system("rm "+bad_runs_file)
    os.system("touch "+ bad_runs_file)
    for i in range(1,num_samples+1):
        data_pathname = globfind(i) 
        r, v_con, y_e_prof, s_prof, r_sh = read1d(data_pathname)
        
        if i == 1:
            global radius_ref
            radius_ref = r
        

        if type(v_con) is not np.ndarray or len(v_con) == 1:
            with open(bad_runs_file, "a+") as br:
                br.write(data_pathname)
                br.write("\n")
        else: 
            r_sh_arr.append(r_sh)
            v_con_arr.append(v_con)
            y_e_arr.append(y_e_prof)
            s_arr.append(s_prof)
    
    r_sh_arr = np.transpose(np.array(r_sh_arr))
    v_con_arr = np.array(v_con_arr)
    y_e_arr = np.array(y_e_arr)
    s_arr = np.array(s_arr)

    global r_sh_emul
    global v_con_emul
    global y_e_emul
    global s_emul

    r_sh_emul.fit(pos_arr,r_sh_arr)
    v_con_emul.fit(pos_arr,v_con_arr)
    y_e_emul.fit(pos_arr,y_e_arr)
    s_emul.fit(pos_arr,s_arr)

def storeEmulators(file1=r_sh_file, file2=v_con_file, file3=y_e_file, file4=s_file):
    with open(file1, "wb") as f1:
        pickle.dump(r_sh_emul, f1, pickle.HIGHEST_PROTOCOL)
    with open(file2, "wb") as f2: 
        pickle.dump(v_con_emul, f2, pickle.HIGHEST_PROTOCOL)
    with open(file3, "wb") as f3: 
        pickle.dump(y_e_emul, f3, pickle.HIGHEST_PROTOCOL)
    with open(file4, "wb") as f4: 
        pickle.dump(s_emul, f4, pickle.HIGHEST_PROTOCOL)
    
def loadEmulators(file1=r_sh_file, file2=v_con_file, file3=y_e_file, file4=s_file):
    r_sh_load = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
    v_con_load = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
    y_e_load = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)
    s_load = gaussian_process.GaussianProcessRegressor(kernel=kernel_choice)


    with open(file1, "rb") as f1:
        r_sh_load = pickle.load(f1)
    with open(file2, "rb") as f2: 
        v_con_load = pickle.load(f2)
    with open(file3, "rb") as f3: 
        y_e_load = pickle.load(f3)
    with open(file4, "rb") as f4: 
        s_load = pickle.load(f4)

    global r_sh_emul
    global v_con_emul
    global y_e_emul
    global s_emul

    r_sh_emul = r_sh_load
    v_con_emul = v_con_load
    y_e_emul = y_e_load
    s_emul = s_load 

def radii():
    return radius_ref
    
def emulRShock(arr): #Should be fed one set of n parameters or n arrays of parameters
    arr = resh(arr)
    out_arr = r_sh_emul.predict(arr,return_std=True)
    return out_arr[0][0], out_arr[1][0]
def emulVCon(arr):
    arr = resh(arr)
    out_arr = v_con_emul.predict(arr,return_std=True)
    return out_arr[0][0], out_arr[1][0]

def emulYE(arr):
    arr = resh(arr)
    out_arr = y_e_emul.predict(arr,return_std=True)
    return out_arr[0][0], out_arr[1][0]

def emulS(arr):
    arr = resh(arr)
    out_arr = s_emul.predict(arr,return_std=True)
    return out_arr[0][0], out_arr[1][0]

if __name__ == '__main__':
    calibrateEmulators(trial_directory)
    storeEmulators()
