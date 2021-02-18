#!/usr/bin/env python3
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1' 
os.environ['MKL_NUM_THREADS'] = '1'

## these linesline if you want to use the git version of the code, instead of the one installed by pip
local_code = True
num_proc = 8

print(os.listdir())

import os

if local_code:
   if 'wannierberri' not in os.listdir() :
       os.symlink("../wannierberri", "wannierberri") # symlink(src, dst) : symbolic link dst pointing to src.
else:
   if 'wannierberri' in os.listdir() :
       os.remove('wannierberri')

if 'Fe_tb.dat' not in os.listdir():
    os.system('tar -xvf ../data/Fe_tb.dat.tar.gz')


import wannierberri as wberri

import numpy as np


SYM = wberri.symmetry

Efermi = np.linspace(12., 13., 101)
system = wberri.System_tb(tb_file='data/Fe_tb.dat', berry=True)
# read all information from a file Fe_tb.dat, which is also written by Wannier90, or maybe composed by user from any tight-binding model.

# system = wberri.System_w90('Fe', berry=True)
# read the information about Wanier functions
generators = [SYM.Inversion, SYM.C4z, SYM.TimeReversal*SYM.C2x]
# B_ext along z => inversion, 4fold rotation around z and TR combined with 2fold rotation around x-axis
system.set_symmetry(generators)

grid = wberri.Grid(system, length=20) # spacing is approx 2pi/length - here grid of 52^3 for length=200 and depends on unit cell size

wberri.integrate(system, grid=grid, Efermi=Efermi,
            smearEf=10, # 10K = 10 Kelvin to avoid strong jittering of the curve
            quantities=["ahc","dos","cumdos"], # calculation of AHC, DOS and cumulated DOS
            numproc=num_proc,
            adpt_num_iter=10, # number of iterations for an adaptive recursive refinement algorithm to make the calculation more precise around those points where it diverges,
            fftlib='fftw', #default.  alternative  option - 'numpy'
            fout_name='Fe',
            restart=False,
            )


# wberri.tabulate(system, grid=grid, quantities=["berry"],
#              frmsf_name='Fe',
#              numproc=num_proc,
#              ibands=np.arange(4, 10),  # energies and Berry curvature of bands 4,5,6,7,8,9
#              EF0=12.6)
