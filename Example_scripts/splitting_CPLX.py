#!/usr/bin/env python3

from ase.io import read,write
import os


# For a new CPLX system file called rcplx.vasp (taking 09-REC-50-OM as an example)

#Step1 split into subsystems
s=read('rcplx.vasp')
n_tot = s.get_global_number_of_atoms()
n_om=20
n_rec=60
n_gra=200

os.makedirs('ORCA_om',exist_ok=True)
os.makedirs('ORCA_dm',exist_ok=True)
os.makedirs('ORCA_rec',exist_ok=True)

s[n_gra + n_rec : n_gra + n_rec + n_om].write('./ORCA_om/rcplx.vasp') #OM ORCA
s[n_gra : n_gra + n_rec].write('./ORCA_rec/rcplx.vasp') #REC ORCA
s[n_gra : n_gra + n_rec + n_om].write('./ORCA_dm/rcplx.vasp') #DM ORCA

#Step2 Do ORCA and for each system 
VASP_sys = [i for i in os.listdir() if 'VASP' in i]
ORCA_sys = [i for i in os.listdir() if 'ORCA' in i]

