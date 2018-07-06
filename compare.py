from emulators import *
import matplotlib.pyplot as plt
from settings import *
from read1d import *
from read3d import *
import argparse
import glob

sim_num = 1
pathname = "/mnt/research/SNAPhU/STIR/parameter_study/calib2/run_mcmcPS_20_a0.343333_b0.22/output/"
lcomp = 0.7983325666666667
dcomp = 0.4183353
r = []
plot1_v = []
plot1_y = []
plot1_s = []
r_sh_1D = 0

parser = argparse.ArgumentParser(description="Compare 1D to 3D simulations")
parser.add_argument('--sim', action='store', nargs=1)
parser.add_argument('--emul', action='append', nargs=5)
args = parser.parse_args()

if args.sim != None:
    sim_num = int(args.sim[0])
    pathname = globfind(sim_num)
    r, plot1_v, plot1_y, plot1_s, r_sh_1D = read1d(pathname)
    plot1_v = np.transpose(plot1_v)
    plot1_y = np.transpose(plot1_y)
    plot1_s = np.transpose(plot1_s)

elif args.emul != None:
    lcomp = float(args.emul[0][0])
    d1comp = float(args.emul[0][1])
    d2comp = float(args.emul[0][2])
    d3comp = float(args.emul[0][3])
    d4comp = float(args.emul[0][4])

    loadEmulators()


    params = np.reshape(np.array([[lcomp,d1comp,d2comp,d3comp,d4comp]]),(1,-1))
    plot1_v, plot1_v_std = emulVCon(params)
    plot1_y, plot1_y_std = emulYE(params)
    plot1_s, plot1_s_std = emulS(params)
    r = radii()
    r_sh_1D = emulRShock(params)[0]

r_sh_3D, r_3D, v_con_3D, y_e_3D, s_3D = readOutput(data_dir3D)

print("Shock radius (1D) = "+str(r_sh_1D))
print("Shock radius (3D) = "+str(r_sh_3D))

plt.figure("Convective Velocity")
#print(r.shape)
#print(r)
#print(len(r_3D))
#print(r_3D)

#print(plot1_v)
#print(plot1_y)
#print(plot1_s)
plt.plot(r_3D,plot1_v, color = 'b', label='1D') 
plt.plot(r_3D,v_con_3D, color = 'g', label = '3D')
plt.legend()
plt.xlabel("Radius (cm)")
plt.ylabel("Convective velocity (cm/s)")

plt.figure("Electron Fraction")
plt.plot(r_3D,plot1_y, color = 'b', label='1D') 
plt.plot(r_3D,y_e_3D, color = 'g', label='3D')
plt.legend()
plt.xlabel("Radius (cm)")
plt.ylabel("Electron fraction")

plt.figure("Entropy")
plt.plot(r_3D,plot1_s, color = 'b', label='1D') 
plt.plot(r_3D,s_3D, color = 'g', label='3D')
plt.legend()
plt.xlabel("Radius (cm)")
plt.ylabel("Entropy (k_B/baryon)")

plt.show() 
