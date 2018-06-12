#!/usr/bin/env python
# ----------------------------------------------------------------
#
#  Creates the job submission script and flash.par
#  files for running the various simulations.
#  Tailored for use in the MCMC Parameter Study
#
#  3D Shock Radius Data:
#    /mnt/research/SNAPhU/STIR/mesa20/mesa20_v_LR.dat
#  3D Other: /mnt/research/SNAPhU/STIR/3dData/
#    vconData, profileData.
#  1D Data: /mnt/research/SNAPhU/STIR/run_mesa20/output_may6_b*
#
# ----------------------------------------------------------------
import io
import os
import shutil
import simfiles
import numpy as np
from settings import *

# ----------------------------------------
#  We will want to read in all of the
#  alpha values from input files.
# ----------------------------------------
#path = "/mnt/research/SNAPhU/STIR/run_ps/"
path = "./"
paramFile = os.path.join(path,"positions_cp.txt")
param = np.loadtxt(paramFile)
alphaL = param[:,0]
alphaD = param[:,1]

#alphaL = (0.0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4)
#alphaD = (0.3333333333, 0.666666666)
runname = "mcmcPS"
restart = False
mcmcRun = "1"

#for (a,b) in [(a,b) for a in alphaL for b in alphaD]:
for a,b in zip(alphaL,alphaD):
    i = 1 # counter for file names

    #mass = (9.0,9.25,9.5,9.75,10.0,10.25,10.5,10.75,11.0,11.25,11.5,11.75,12.0,12.25,12.5,12.75,13.0, \
    #            13.1,13.2,13.3,13.4,13.5,13.6,13.7,13.8,13.9, \
    #            14.0,14.1,14.2,14.3,14.4,14.5,14.6,14.7,14.8,14.9, \
    #            15.0,15.1,15.2,15.3,15.4,15.5,15.6,15.7,15.8,15.9, \
    #            16.0,16.1,16.2,16.3,16.4,16.5,16.6,16.7,16.8,16.9, \
    #            17.0,17.1,17.2,17.3,17.4,17.5,17.6,17.7,17.8,17.9, \
    #            18.0,18.1,18.2,18.3,18.4,18.5,18.6,18.7,18.8,18.9, \
    #            19.0,19.1,19.2,19.3,19.4,19.5,19.6,19.7,19.8,19.9, \
    #            20.0,20.1,20.2,20.3,20.4,20.5,20.6,20.7,20.8,20.9, \
    #            21.0,21.1,21.2,21.3,21.4,21.5,21.6,21.7,21.8,21.9, \
    #            22.0,22.1,22.2,22.3,22.4,22.5,22.6,22.7,22.8,22.9, \
    #            23.0,23.1,24.0,25.0,26.0,27.0,28.0,29.0, \
    #            30.0,31,32,33,35,40,45,50,55,60,70,80,100,120)
    mass = [20.0]

    path1 = "run_"+runname+"_step"+str(mcmc_step)+str(i)+"_a"+str(a)+"_b"+str(b) # Sets the name of the run.
    if not os.path.isdir(path1): # returns true if a directory exists.
        os.makedirs(path1) # Creates a run directory if it doesn't exist
    filename = "run.mlt"
    fullpath = os.path.join(path1, filename)
    # ----------------------------------------
    #  This loop writes the bash script to run
    #  the simulations.
    # ----------------------------------------
    with io.FileIO(fullpath, "w") as file:
            file.write("#!/bin/bash -login\n")
            file.write("\n")
            file.write("### define resources needed:\n")
            file.write("### walltime - how long you expect the job to run\n")
            file.write("#PBS -l walltime=24:00:00\n")
            file.write("\n")
            file.write("### nodes:ppn - how many nodes & cores per node (ppn) that you require\n")
            file.write("#PBS -l nodes=1:ppn=2,feature=intel16\n")
            file.write("\n")
            file.write("### mem: amount of memory that the job will need\n")
            file.write("#PBS -l mem=4gb\n")
            file.write("#PBS -A ptg\n") # Can Theo and I use this?
            file.write("###Batch job\n")
           # file.write("#PBS -t 1-138\n") # Will have to edit this
            file.write("### you can give your job a name for easier identification\n")
            file.write("#PBS -N param_study"+str(a)+"_"+str(b)+"\n")
            file.write("\n")
            file.write("### load necessary modules, e.g.\n")
            file.write("module purge\n")
            file.write("module load Intel/16.3\n")
            file.write("module load OpenMPI/2.0.1\n")
            file.write("module load HDF5/1.8.18\n")
            file.write("\n")
            file.write("### change to the working directory where your code is located\n")
            # --- Change this On Runtime ---
            file.write("cd /mnt/research/SNAPhU/STIR/run_ps/"+path1+"/output${PBS_ARRAYID}\n")
            file.write("\n")
            file.write("### call your executable\n")
            file.write("mpirun -np 2 flash4 \n")
    ## Copy FLASH executable to run directory once, then symlink to m directories
    #dest = os.path.join(path1,"flash4")
    #if os.path.isfile(dest):
    #    print('file exists')
    #    os.remove(dest)
    ## Source for flash executable:
    #src = "/mnt/research/SNAPhU/STIR/run_sukhbold/flash4_1f31289"
    #shutil.copy(src,dest)

    # --- Do We Need This? ---
    # I think that we do not need loops over mass.
    # Creates output files labelled by mass.

    for m in mass:
        path = "output"#+str(mass.index(m)+1) # We don't need so many
        dest1 = os.path.join(path1,path)
        if not os.path.isdir(dest1):
    		os.makedirs(dest1)
        out = "output"
        #outfull = os.path.join(dest1, out)
        outfull = dest1 # Just one output directory in the run directory.
        if not os.path.isdir(outfull):
               os.makedirs(outfull)
        ## Now make symlinks to copied executable
        src = "/mnt/research/SNAPhU/STIR/run_ps/flash4_1f312899"#-l9
        dest = os.path.join(dest1,"flash4")
        if os.path.isfile(dest):
               os.remove(dest)
        os.symlink(src,dest)
        print(dest)
        ## EOS table
    	dest = os.path.join(dest1,"SFHo.h5")
        if os.path.isfile(dest):
                print('file exists')
                os.remove(dest)
    ## Source for eos table:
	src = "/mnt/research/SNAPhU/Tables/SFHo.h5"
	os.symlink(src,dest)
	dest = os.path.join(dest1,"NuLib_SFHo.h5")
        if os.path.isfile(dest):
                print('file exists')
                os.remove(dest)
    ## Source for opacity table:
	src = "/mnt/research/SNAPhU/Tables/NuLib_SFHo_noweakrates_rho82_temp65_ye60_ng12_ns3_Itemp65_Ieta61_version1.0_20170719.h5"
	os.symlink(src,dest)
	dest = os.path.join(dest1,"s"+str(m)+"_5mspb.FLASH")
        if os.path.isfile(dest):
                print('file exists')
                os.remove(dest)
    ## Source for progenitor:
	src = os.path.join("/mnt/research/SNAPhU/Progenitors2","s"+str(m)+"_5mspb.FLASH")
	os.symlink(src,dest)
	path = os.path.join(dest1,"output")
    	if restart:
            path = os.path.join(path,"stir_"+runname+"_s"+str(m)+"_alpha"+str(a))
            myFiles = simfiles.FlashOutputFiles(path)
            myChkfiles = myFiles.chkFilePaths()
            files = [chkfiles for chkfiles in myChkfiles]
            print "last checkpoint:", files[-1]
            refile = files[-1]
	    refile = refile[-4:]

        filename = "flash.par"
        fullpath = os.path.join(dest1, filename)
        # ----------------------------------------
        #  Write the flash.par file
        # ----------------------------------------
        with io.FileIO(fullpath, "w") as file:
            file.write("# Parameters file for 1D M1 Core Collapse with MLT\n")
            file.write("basenm			         = \"stir_"+runname+"_s"+str(m)+"_alpha"+str(a)+"_\"\n")
            if restart:
                file.write("restart			        = .true.\n")
                file.write("checkpointFileNumber           = "+str(refile)+"\n")
            else:
                file.write("restart                 = .false.\n")
                file.write("checkpointFileNumber            = 0000 \n")
            file.write("plotFileNumber                 = 0\n")
            file.write("output_directory	        = \"output\"\n")
            file.write("\n")
            file.write("# IO\n")
            file.write("wr_integrals_freq		= 20\n")
            file.write("checkpointFileIntervalStep     = 0\n")
            file.write("checkpointFileIntervalTime     = 0.01\n")
            file.write("plotFileIntervalStep           = 0\n")
            file.write("plotFileIntervalTime           = 0.00\n")
            file.write("particleFileIntervalTime       = 0.000\n")
            file.write("wall_clock_time_limit          = 86000\n")
            file.write("\n")
            file.write("#particles\n")
            file.write("useparticles = .false.\n")
            file.write("pt_dtfactor = 0.5\n")
            file.write("pt_numR = 200\n")
            file.write("pt_numT = 160\n")
            file.write("pt_numP = 1\n")
            file.write("\n")
            file.write("pt_initialRMin = 1.97d8 #unique to every progenitor and t_init, center around region of interest\n")
            file.write("pt_initialRMax = 7.0d8 #unique to every progenitor and t_init, center around region of interest\n")
            file.write("pt_initialCTMin = -1.0d0\n")
            file.write("pt_initialCTMax = 1.0d0\n")
            file.write("pt_initialPMin = 0.0d0\n")
            file.write("pt_initialPMax = 6.2831853072d0\n")
            file.write("pt_maxPerProc = 32000\n")
            file.write("\n")
            file.write("# Time\n")
            file.write("tinitial                       = 0.005\n")
            file.write("tmax                           = 1.50\n") # May need to change
            file.write("nend                           = 1000000000\n")
            file.write("#nend                           = 1\n")
            file.write("tstep_change_factor            = 1.05\n")
            file.write("dtinit                         = 1.E-8\n")
            file.write("dtmax                          = 1.E5\n")
            file.write("dtmin                          = 1.E-20\n")
	        #file.write("useHPCC				= .false.\n") # What's this?
            file.write("\n")
            file.write("# Domain\n")
            file.write("geometry                       = \"spherical\"\n")
            file.write("xmin                           = 0.0\n")
            if (m == 9.0 or m==9.25):
               file.write("xmax                           = 1.3e9\n")
            else:
               file.write("xmax                           = 1.5e9\n")
            file.write("xl_boundary_type               = \"reflect\"\n")
            file.write("xr_boundary_type               = \"user\"\n")
            file.write("\n")
            file.write("# Grid/Refinement\n")
            file.write("nblockx                        = 8\n")
            file.write("nblocky                        = 1\n")
            file.write("nblockz                        = 1\n")
            file.write("\n")
            file.write("gr_lrefineMaxRedDoByLogR       = .true.\n")
            file.write("gr_angularResolution           = 0.4\n")
            file.write("lrefine_max                    = 9\n")
            file.write("lrefine_min                    = 1\n")
            file.write("refine_var_1                   = \"dens\"\n")
            file.write("refine_var_2                   = \"pres\"\n")
            file.write("refine_var_3                   = \"none\"\n")
            file.write("refine_var_4                   = \"none\"\n")
            file.write("refine_cutoff_1		       = 0.8\n")
            file.write("refine_cutoff_2		       = 0.8\n")
            file.write("refine_cutoff_3		       = 0.8\n")
            file.write("refine_cutoff_4		       = 0.8\n")
            file.write("\n")
            file.write("# Simulation\n")
            file.write("model_file = \"s"+str(m)+"_5mspb.FLASH\"\n")
            file.write("#rnd_seed			= 1000\n")
            file.write("#rnd_scale 			= 0.001\n")
            file.write("nsub                           = 4\n")
            file.write("vel_mult                       = 1.0\n")
            file.write("ener_exp                       = 0.0\n")
            file.write("r_exp_max                      = 0.0\n")
            file.write("r_exp_min                      = 0.0\n")
            file.write("mass_loss                      = 1.0e-4 # Solar masses per year\n")
            file.write("vel_wind                       = 1.0e4  # cm/s\n")
            file.write("use_PnotT		       = .FALSE.\n")
            file.write("rot_a			       = 8.0e7\n")
            file.write("rot_omega		       = 0.\n")
            file.write("use_perturb		       = .false.\n")
            file.write("mag_e			       = 1.0e18\n")
            file.write("perturb_radMax		       = 2.4e8\n")
            file.write("perturb_radMin		       = 1.82952e8\n")
            file.write("perturb_nodes		       = 5\n")
            file.write("perturb_mag		       = 0.2\n")
            file.write("mri_refine		       = .false.\n")
            file.write("mri_time		       = 0.0\n")
            file.write("alwaysRefineShock	       = .false.\n")
            file.write("\n")
            file.write("# Hydro\n")
            file.write("useHydro                       = .TRUE.\n")
            file.write("cfl                            = 0.5\n")
            file.write("interpol_order                 = 2\n")
            file.write("updateHydroFluxes              = .TRUE.\n")
            file.write("eintSwitch		       = 0.0 # Always use Etot\n")
            file.write("#convertToConsvdForMeshCalls   = .false.\n")
            file.write("#converttoconsvdinmeshinterp   = .false.\n")
            file.write("\n")
            file.write("##  SWITCHES SPECIFIC TO THE UNSPLIT HYDRO SOLVER               ##\n")
            file.write("#       I. INTERPOLATION SCHEME:\n")
            file.write("order           = 3      # Interpolation order (first/second/third/fifth order)\n")
            file.write("slopeLimiter    = \"hybrid\"   # Slope limiters (minmod, mc, vanLeer, hybrid, limited)\n")
            file.write("LimitedSlopeBeta= 1.     # Slope parameter for the \"limited\" slope by Toro\n")
            file.write("charLimiting    = .true. # Characteristic limiting vs.Primitive limiting\n")
            file.write("\n")
            file.write("use_avisc       = .true. # use artificial viscosity (originally for PPM)\n")
            file.write("cvisc           = 0.2   # coefficient for artificial viscosity\n")
            file.write("use_flattening  = .true. # use flattening (dissipative) (originally for PPM)\n")
            file.write("use_steepening  = .false. # use contact steepening (originally for PPM)\n")
            file.write("use_upwindTVD   = .false. # use upwind biased TVD slope for PPM (need nguard=6)\n")
            file.write("flux_correct    = .true.\n")
            file.write("\n")
            file.write("#       II. RIEMANN SOLVERS:\n")
            file.write("RiemannSolver   = \"HLLC\"       # Roe, HLL, HLLC, LLF, Marquina\n")
            file.write("entropy         = .false.     # Entropy fix for the Roe solver\n")
            file.write("EOSforRiemann   = .true.\n")
            file.write("use_hybridRiemann = .true.\n")
            file.write("\n")
            file.write("#       III. STRONG SHOCK HANDELING SCHEME:\n")
            file.write("shockDetect     = .true.     # Shock Detect for numerical stability\n")
            file.write("shockLowerCFL 	= .false.\n")
            file.write("\n")
            file.write("## -------------------------------------------------------------##\n")
            file.write("\n")
            file.write("# Gravity\n")
            file.write("useGravity                     = .true.\n")
            file.write("updateGravity                  = .TRUE.\n")
            file.write("grav_boundary_type             = \"isolated\"\n")
            file.write("mpole_3daxisymmetry            = .false.\n")
            file.write("mpole_dumpMoments              = .FALSE.\n")
            file.write("mpole_PrintRadialInfo	       = .false.\n")
            file.write("mpole_IgnoreInnerZone	       = .false.\n")
            file.write("mpole_lmax                     = 0\n")
            file.write("mpole_ZoneRadiusFraction_1     = 1.0\n")
            file.write("mpole_ZoneExponent_1           = 0.005\n")
            file.write("mpole_ZoneScalar_1	       = 0.5\n")
            file.write("mpole_ZoneType_1	       = \"logarithmic\"\n")
            file.write("point_mass                     = 0.0\n")
            file.write("point_mass_rsoft               = 0.e0\n")
            file.write("use_gravHalfUpdate             = .TRUE.\n")
            file.write("use_gravConsv		       = .FALSE.\n")
            file.write("use_gravPotUpdate	       = .FALSE.\n")
            file.write("mpole_useEffectivePot          = .true.\n")
            file.write("mpole_EffPotNum 	       = 1000\n")
            file.write("\n")
            file.write("# Hole\n")
            file.write("useHole			       = .FALSE.\n")
            file.write("hole_radius		       = 90e5 #2.0e8\n")
            file.write("hole_bnd		       = 1 #diode=0, reflect=1, outflow=2\n")
            file.write("hole_time		       = 0.0 #3.0\n")
            file.write("hole_vel		       = 0.0 #1.0e7\n")
            file.write("\n")
            file.write("# Nuclear Burning\n")
            file.write("#useBurn                        = .FALSE.\n")
            file.write("#useBurnTable                   = .FALSE.\n")
            file.write("#burnUpdateEint		       = .FALSE.\n")
            file.write("#enucDtFactor                   = 1.e30\n")
            file.write("#nuclearDensMax                 = 1.0E14\n")
            file.write("#nuclearDensMin                 = 1.0E-10\n")
            file.write("#nuclearNI56Max                 = 1.0\n")
            file.write("#nuclearTempMax                 = 1.0E12\n")
            file.write("#nuclearTempMin                 = 1.1E8\n")
            file.write("#odeStepper                     = 1\n")
            file.write("#algebra                        = 2\n")
            file.write("#useShockBurn                   = .FALSE.\n")
            file.write("\n")
            file.write("#MLT\n")
            file.write("useMLT = .true.\n")
            file.write("mlt_alphaL = "+str(a)+"\n")
            file.write("mlt_alphaD = "+str(b)+"\n")
            file.write("\n")
            file.write("# EOS\n")
            file.write("eos_file = \"./SFHo.h5\"\n")
            file.write("eosMode                        = \"dens_ie\"\n")
            file.write("eosModeInit                    = \"dens_temp\"\n")
            file.write("#eos_coulombAbort               = .true.\n")
            file.write("#eos_coulombMult                = 0.0\n")
            file.write("#eos_forceConstantInput         = .false.\n")
            file.write("#eos_maxNewton                  = 50\n")
            file.write("#eos_singleSpeciesA             = 1.00\n")
            file.write("#eos_singleSpeciesZ             = 1.00\n")
            file.write("#eos_tolerance                  = 1.e-8\n")
            file.write("gamma                          = 1.2\n")
            file.write("#eos_table_tmax			= 50.\n")
            file.write("\n")
            file.write("# Deleptonization\n")
            file.write("useDeleptonize		       = .false.\n")
            file.write("delep_Enu		       = 10.0 # MeV\n")
            file.write("delep_rhoOne		       = 3.0e7 #3.0e7\n")
            file.write("delep_rhoTwo		       = 2.0e13 #2.0e13\n")
            file.write("delep_rhoThree		       = 2.0e14 \n")
            file.write("delep_yOne		       = 0.5\n")
            file.write("delep_yTwo		       = 0.278 #0.278\n")
            file.write("delep_yc		       = 0.035 #0.035\n")
            file.write("bounceTime		       = 0.0 #0.248\n")
            file.write("postBounce		       = .true.\n")
            file.write("useEntr 		       = .true.\n")
            file.write("\n")
            file.write("# RadTrans/M1\n")
            file.write("rt_useRadTrans			= .true.\n")
            file.write("rt_NumGroups			= 12 #must match m1_groups used in setup\n")
            file.write("rt_opacTable			= \"./NuLib_SFHo.h5\"\n")
            file.write("rt_dtFactor			= 0.3d0\n")
            file.write("rt_fluxCorrect 			= .false. \n")
            file.write("rt_rkTime			= .false. \n")
            file.write("rt_doVel			= .true.\n")
            file.write("rt_pushFac			= 1.0d0\n")
            file.write("\n")
            file.write("# Neutrino Heating/Cooling\n")
            file.write("useHeat			       = .false.\n")
            file.write("Lneut			       = 2.2e52\n")
            file.write("Tneut			       = 4.0 #MeV\n")
            file.write("heatTimeFac		       = 1.0e4\n")
            file.write("useHalfState		       = .false.\n")
            file.write("\n")
            file.write("# EnergyDeposition - Jets\n")
            file.write("useEnergyDeposition	       = .FALSE.\n")
            file.write("#jetAngleN		       = 0.52\n")
            file.write("#jetAngleS		       = 0.52\n")
            file.write("#jetAccN			       = 5.0e10\n")
            file.write("#jetAccS			       = 1.0e10\n")
            file.write("#jetTimeN		       = 2.0\n")
            file.write("#jetTimeS		       = 0.0\n")
            file.write("#jetRad			       = 4.0e8\n")
            file.write("#heat_fact		       = 1.0\n")
            file.write("			      			       \n")
            file.write("# Small numbers\n")
            file.write("smallt                         = 1.2e8\n")
            file.write("smlrho                         = 1.1e3\n")
            file.write("smallp                         = 1.E-20\n")
            file.write("smalle                         = 1.E1\n")
            file.write("\n")
            file.write("smallu                         = 1.E-10\n")
            file.write("smallx                         = 1.E-100\n")
            file.write("small                          = 1.E-100\n")
i = i + 1
