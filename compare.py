from emulators import *
import matplotlib.pyplot as plt
import matplotlib
from settings import *
from read1d import *
from read3d import *
import argparse
import glob

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)

sim_num = 1
pathname = "/mnt/research/SNAPhU/STIR/parameter_study/calib2/run_mcmcPS_20_a0.343333_b0.22/output/"
lcomp = 0.7983325666666667
dcomp = 0.4183353
r = []
plot1_v = []
plot1_y = []
plot1_s = []
r_sh_1 = 0
plot1_v_std = []
plot1_y_std = []
plot1_s_std = []

plot2_v = []
plot2_y = []
plot2_s = []
r_sh_2 = 0
plot2_v_std = []
plot2_y_std = []
plot2_s_std = []

parser = argparse.ArgumentParser(description="Compare 1D to 3D simulations")
parser.add_argument('--sim', action='store', nargs=1)
parser.add_argument('--emul', action='append', nargs=5)
args = parser.parse_args()

sim = args.sim != None
emul = args.emul != None

if sim:
    sim_num = int(args.sim[0])
    pathname = globfind(sim_num, trial_directory_2)
    r, plot1_v, plot1_y, plot1_s, r_sh_1 = read1d(pathname)
    plot1_v = np.transpose(plot1_v)
    plot1_v_std = 0.05*plot1_v
    plot1_y = np.transpose(plot1_y)
    plot1_y_std = 0.05*plot1_y
    plot1_s = np.transpose(plot1_s)
    plot1_s_std = 0.05*plot1_s
    r_sh_1_std = 0.05*r_sh_1

if emul:
    lcomp = float(args.emul[0][0])
    d1comp = float(args.emul[0][1])
    d2comp = float(args.emul[0][2])
    d3comp = float(args.emul[0][3])
    d4comp = float(args.emul[0][4])

    loadEmulators()


    params = np.reshape(np.array([[lcomp,d1comp,d2comp,d3comp,d4comp]]),(1,-1))
    plot2_v, plot2_v_std = emulVCon(params)
    plot2_y, plot2_y_std = emulYE(params)
    plot2_s, plot2_s_std = emulS(params)

    r = radii()
    r_sh_2, r_sh_2_std = emulRShock(params)

r_sh_3D, r_3D, v_con_3D, y_e_3D, s_3D = readOutput(data_dir3D)

if sim:
    print("Shock radius (1D) = "+str(r_sh_1)+" +/- "+str(r_sh_1_std))
if emul:
    print("Shock radius (1D emulator) = "+str(r_sh_2)+" +/- "+str(r_sh_2_std))
    
print("Shock radius (3D) = "+str(r_sh_3D))

plt.figure("Convective Velocity")

if sim:
    plt.plot(r_3D,plot1_v, color = 'b', label='1D') 
    #plt.fill_between(r_3D, plot1_v-plot1_v_std, plot1_v+plot1_v_std, alpha=0.2)
    plt.axvline(r_sh_1, linestyle=':', color='b', label="shock radius 1D")
if emul: 
    plt.plot(r_3D,plot2_v, color = 'g', label='1D emulator') 
    plt.fill_between(r_3D, plot2_v-plot2_v_std, plot2_v+plot2_v_std, alpha=0.2)
    plt.axvline(r_sh_2, linestyle=':', color='g', label="shock radius 1D emulator")
plt.plot(r_3D,v_con_3D, color = 'k', label = '3D')
plt.legend(fontsize=14)
plt.title("Convective velocity at distance from center", fontsize=17)
plt.xlabel("Radius (cm)")
plt.ylabel("Convective velocity (cm/s)")

plt.figure("Electron Fraction")
if sim:
    plt.plot(r_3D,plot1_y, color = 'b', label='1D') 
    #plt.fill_between(r_3D, plot1_y-plot1_y_std, plot1_y+plot1_y_std, alpha=0.2)
if emul: 
    plt.plot(r_3D,plot2_y, color = 'g', label='1D emulator') 
    plt.fill_between(r_3D, plot2_y-plot2_y_std, plot2_y+plot2_y_std, alpha=0.2)
plt.plot(r_3D,y_e_3D, color = 'k', label='3D')
plt.legend()
plt.title("Electron fraction at distance from center")
plt.xlabel("Radius (cm)")
plt.ylabel("Electron fraction")

plt.figure("Entropy")
if sim:
    plt.plot(r_3D,plot1_s, color = 'b', label='1D') 
    #plt.fill_between(r_3D, plot1_s-plot1_s_std, plot1_s+plot1_s_std, alpha=0.2)
if emul: 
    plt.plot(r_3D,plot2_s, color = 'g', label='1D emulator') 
    plt.fill_between(r_3D, plot2_s-plot2_s_std, plot2_s+plot2_s_std, alpha=0.2)
plt.plot(r_3D,s_3D, color = 'k', label='3D')
plt.legend()
plt.title("Entropy at distance from center")
plt.xlabel("Radius (cm)")
plt.ylabel("Entropy (k_B/baryon)")

plt.show() 
