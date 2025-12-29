#!/usr/bin/env python3

from ase.io import read,write
import os
import numpy as np
# ------------------------------- #

# This code is to get RG for mol

# Rg is defined as : (\sigma m_i * r_i^2)/(\sigma m_i)

# ------------------------------- #
def get_rg(file_mol) -> float:
    #file_mol = [file for file in os.listdir() if '.xyz' in file]
    mol = read(file_mol)
    mol.center()
    com = np.dot(mol.get_masses(),mol.get_positions())/mol.get_masses().sum()
    masses_sum = mol.get_masses().sum()
    #get the sum_of_squares
    sum_of_squares = sum(mol.get_masses()[i] * np.linalg.norm(mol.get_positions()[i] - com)**2 for i in range(len(mol)))
    #get the Rg^2
    Rg_2 = sum_of_squares / masses_sum 
    return np.sqrt(Rg_2)


if __name__ == "__main__": 
    Rg = get_rg('96_om.xyz')
    print(Rg)
    print('Unit is angstrom')
