# Functions for calibrating and 
# returning emulators
# 
#----------------------------------


import numpy as np
from sklearn import gaussian_process
from helper_functions import *
from read1d import *

#initialize emulators
r_sh_emul = gaussian_process.GaussianProcessRegressor(kernel="RBF(0.05)")
v_con_emul = gaussian_process.GaussianProcessRegressor(kernel="RBF(0.05)")
y_e_emul = gaussian_process.GaussianProcessRegressor(kernel="RBF(0.05)")
s_emul = gaussian_process.GaussianProcessRegressor(kernel="RBF(0.05)")

def calibrateEmulators(pos_pathname, data_dir): #positions file should have same format as positions.txt
    #data directory contains all run directories from calibration run
    pos_arr = np.array(readPositions(pos_pathname)[0])
    num_samples = pos_arr.shape[0]
    
    #list of radius values, for reference
    radius_ref = []
    #shock radius column vector
    r_sh_arr = []
    #2d arrays containing v_con vectors
    v_con_arr = []
    y_e_arr = []
    s_arr = []
    
    for i in range(1,num_samples+1)
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
