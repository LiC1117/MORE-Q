#!/usr/bin/env python3

import sys
import numpy as np
import pandas as pd
import re
import json
from ase.io import read,write
from get_rg import get_rg
from get_inertia_tensor import get_inertia_tensor
import os
import h5py
#from mace.calculators import mace_off


# -------------------------------------#

# This code is extract ALL SINGLE properties from ORCA by SCF

# -------------------------------------#

def get_data(output): 
    global ha2eV 
    ha2eV = 27.2107
    global kcal2eV 
    kcal2eV = 0.0433634

    with open(output,'r') as f:
        lines = f.read().splitlines()
    C =coordinates(lines)
    clength = len(C[1])
    E_tot = total_energy(lines)
    E_components = energy_components(lines)
    E_HOMO = Orbital_energy(lines)[0]
    E_LUMO = Orbital_energy(lines)[1]
    HL_gp = Orbital_energy(lines)[2]
    HL_energies = Orbital_energy(lines)[3]
    C6 = disp_coef(lines)
    DP_comps = DP_components(lines)[0]
    Dp_tot = DP_components(lines)[1]
    RS_comps = Rotational_Spectrum(lines)
    QP_comps = QP_components(lines)
    QP_tot_ = QP_tot(lines)
    PA_tensor_ = PA_tensor(lines)
    Iso_PA_ = Iso_PA(lines)
    Rg_ = Rg()
    Im_ = Im()
    Q_at_MK_ = Q_at_MK(lines)
    Q_at_LW_ = Q_at_LW(lines)
    Q_at_MY_ = Q_at_MY(lines)
    F = F_atm(lines)
    E_AT = E_atom()
    GEO = get_cmbdf()
    E_BD = E_bd()
    
    

    #check complety of dataset
    lock = 0
    if not C:
        print('Missing Coordinates!')
    else:
        lock += 1
    if isinstance(E_tot,float):
        lock += 1
    else:
        print('Missing Total energy (eV)')
    if len(E_components) == 13:
        lock += 1
    else:
        print('Missing energy component(s)')
    if isinstance(E_components['Edisp'],float):
        lock += 1
    else:
        print('Missing dispersion energy')
    if len(HL_energies) == 22:
        lock += 1
    else:
        print('Missing HOMO/LUMO energies')
    if isinstance(C6,float):
        lock += 1
    else:
        print('Missing C6 value')
    if len(DP_comps) == 9: 
        lock += 1
    else:
        print('Missing dipole moment components')
    if isinstance(Dp_tot,float):
        lock += 1
    else:
        print('Missing total dipole moment')
    if len(RS_comps) == 6:
        lock += 1
    else:
        print('Missing RS_components')
    if len(QP_comps) == 18:
        lock += 1
    else:
        print('Missing QP components')
    if isinstance(QP_tot_,float):
        lock += 1
    else:
        print('Missing QP_tot')
    if len(PA_tensor_) == 6:
        lock += 1
    else:
        print('Missing PA_tensor')
    if isinstance(Iso_PA_,float):
        lock += 1
    else:
        print('Missing Isotropic polarizability')
    if isinstance(Rg_,float):
        lock += 1
    else:
        print('Missing Radius of gyration')
    if len(Im_) == 3:
        lock += 1
    else:
        print('Missing Intertia tensor')
    if len(Q_at_MK_[1]) == clength:
        lock += 1 
    else:
        print('Missing MK atomic charge')
    if len(Q_at_LW_[1]) == clength:
        lock += 1
    else:
        print('Missing LW atomic charge')
    if len(Q_at_MY_['Atom']) == clength:
        lock += 1
    else:
        print('Missing MY atomic charge')
    if len(F) == clength:
        lock += 1
    else:
        print('Missing Atomic forces')
    if isinstance(E_AT,float):
        lock += 1
    else:
        print('Missing Atomisation energy')
    if len(GEO):
        lock += 1
    else:
        print('Missing cmbdf descriptors')

    #if isinstance(E_BD,float):
    #    lock += 1
    #else:
    #    print('Missing Binding energy')


    #if the complety is fulfilled:
    if lock == 21:
        output_ = {}
        output_['atNUM'] = C[0]
        output_['atXYZ'] = C[1]
        output_['ePBE+D3'] = E_tot
        #output_[''] =  E_components['E_TOT_SCF']
        output_['eNUC'] = round(E_components['NUR'],6)
        output_['eELE'] = round(E_components['ELE'],6)
        output_['e1E'] = round(E_components['1E'],6)
        output_['e2E'] = round(E_components['2E'],6)
        output_['ePE'] = round(E_components['virial_pe'],6)
        output_['eKE'] = round(E_components['virial_ke'],6)
        output_['eX'] = round(E_components['DFT_X'],6)
        output_['eC'] = round(E_components['DFT_C'],6)
        output_['eXC'] = round(E_components['DFT_XC'],6)

        output_['eD3'] = round(E_components['Edisp'],6)
        output_['eE6'] = round(E_components['E6'],6)
        output_['eE8'] = round(E_components['E8'],6)


        output_['eH'] = E_HOMO
        output_['eL'] = E_LUMO
        output_['HLgap'] = round(HL_gp,6)
        output_['eORB'] = HL_energies
        output_['mC6'] = C6
        
        output_['vEDIP'] =  [DP_comps['Electronic contribution X'],DP_comps['Electronic contribution Y'],DP_comps['Electronic contribution Z']]
        #output_['DP_ELE_X'] = DP_comps['Electronic contribution X']
        #output_['DP_ELE_Y'] = DP_comps['Electronic contribution Y']
        #output_['DP_ELE_Z'] = DP_comps['Electronic contribution Z']
        output_['vNDIP'] = [DP_comps['Nuclear contribution X'],DP_comps['Nuclear contribution Y'],DP_comps['Nuclear contribution Z']]
        #output_['DP_NUC_X'] = DP_comps['Nuclear contribution X']
        #output_['DP_NUC_Y'] = DP_comps['Nuclear contribution Y']
        #output_['DP_NUC_Z'] = DP_comps['Nuclear contribution Z']
        output_['vDIP'] = [DP_comps['Total dipole moment contribution X'],DP_comps['Total dipole moment contribution Y'],DP_comps['Total dipole moment contribution Z']]
       # output_['DP_TOT_X'] = DP_comps['Total dipole moment contribution X']
       # output_['DP_TOT_Y'] = DP_comps['Total dipole moment contribution Y']
       # output_['DP_TOT_Z'] = DP_comps['Total dipole moment contribution Z']
        output_['DIP'] = Dp_tot
        output_['vRS'] = [RS_comps['Rational Spectrum X'],RS_comps['Rational Spectrum Y'],RS_comps['Rational Spectrum Z']]
        #output_['RS_X'] = RS_comps['Rational Spectrum X']
        #output_['RS_Y'] = RS_comps['Rational Spectrum Y']
        #output_['RS_Z'] = RS_comps['Rational Spectrum Z']
        output_['vRSDIP'] = [RS_comps['RS dipole X (Debye)'],RS_comps['RS dipole Y (Debye)'], RS_comps['RS dipole Z (Debye)']]
        #output_['RS_DP_X'] = RS_comps['RS dipole X (Debye)']
        #output_['RS_DP_Y'] = RS_comps['RS dipole Y (Debye)']
        #output_['RS_DP_Z'] = RS_comps['RS dipole Z (Debye)']

        output_['NQP'] = [QP_comps['Nuclear contribution XX'],QP_comps['Nuclear contribution YY'],QP_comps['Nuclear contribution ZZ'], QP_comps['Nuclear contribution XY'],QP_comps['Nuclear contribution XZ'],QP_comps['Nuclear contribution YZ']]
        #output_['QP_NUC_XX'] = QP_comps['Nuclear contribution XX']
        #output_['QP_NUC_YY'] = QP_comps['Nuclear contribution YY']
        #output_['QP_NUC_ZZ'] = QP_comps['Nuclear contribution ZZ']
        #output_['QP_NUC_XY'] = QP_comps['Nuclear contribution XY']
        #output_['QP_NUC_XZ'] = QP_comps['Nuclear contribution XZ']
        #output_['QP_NUC_YZ'] = QP_comps['Nuclear contribution YZ']
        output_['EQP'] = [QP_comps['Electronic contribution XX'],QP_comps['Electronic contribution YY'], QP_comps['Electronic contribution ZZ'],QP_comps['Electronic contribution XY'],QP_comps['Electronic contribution XZ'],QP_comps['Electronic contribution YZ']]
        #output_['QP_ELE_XX'] = QP_comps['Electronic contribution XX']
        #output_['QP_ELE_YY'] = QP_comps['Electronic contribution YY']
        #output_['QP_ELE_ZZ'] = QP_comps['Electronic contribution ZZ']
        #output_['QP_ELE_XY'] = QP_comps['Electronic contribution XY']
        #output_['QP_ELE_XZ'] = QP_comps['Electronic contribution XZ']
        #output_['QP_ELE_YZ'] = QP_comps['Electronic contribution YZ']
        output_['TQP'] = [QP_comps['Total quadrupole moment XX'],QP_comps['Total quadrupole moment YY'],QP_comps['Total quadrupole moment ZZ'], QP_comps['Total quadrupole moment XY'],QP_comps['Total quadrupole moment XZ'],QP_comps['Total quadrupole moment YZ']]
        #output_['QP_TOT_XX'] = QP_comps['Total quadrupole moment XX']
        #output_['QP_TOT_YY'] = QP_comps['Total quadrupole moment YY']
        #output_['QP_TOT_ZZ'] = QP_comps['Total quadrupole moment ZZ']
        #output_['QP_TOT_XY'] = QP_comps['Total quadrupole moment XY']
        #output_['QP_TOT_XZ'] = QP_comps['Total quadrupole moment XZ']
        #output_['QP_TOT_YZ'] = QP_comps['Total quadrupole moment YZ']
        output_['mQP'] = QP_tot_
        output_['mTPOL'] = [PA_tensor_['POLARIZABILITY TENSOR XX'],PA_tensor_['POLARIZABILITY TENSOR YY'],PA_tensor_['POLARIZABILITY TENSOR ZZ'],PA_tensor_['POLARIZABILITY TENSOR XY'],PA_tensor_['POLARIZABILITY TENSOR XZ'],PA_tensor_['POLARIZABILITY TENSOR YZ']]
        #output_['PA_XX'] = PA_tensor_['POLARIZABILITY TENSOR XX']
        #output_['PA_YY'] = PA_tensor_['POLARIZABILITY TENSOR YY']
        #output_['PA_ZZ'] = PA_tensor_['POLARIZABILITY TENSOR ZZ']
        #output_['PA_XY'] = PA_tensor_['POLARIZABILITY TENSOR XY']
        #output_['PA_XZ'] = PA_tensor_['POLARIZABILITY TENSOR XZ']
        #output_['PA_YZ'] = PA_tensor_['POLARIZABILITY TENSOR YZ']

        output_['mPOL'] = Iso_PA_
        output_['RG'] = round(Rg_,6)
        output_['IM'] = [round(Im_[0][0],6),round(Im_[1][1],6),round(Im_[2][2],6),round(Im_[0][1],6),round(Im_[0][2],6),round(Im_[1][2],6)]
        #output_['IM_XX'] = Im_[0][0]
        #output_['IM_YY'] = Im_[1][1]
        #output_['IM_ZZ'] = Im_[2][2]
        #output_['IM_XY'] = Im_[0][1]
        #output_['IM_XZ'] = Im_[0][2]
        #output_['IM_YZ'] = Im_[1][2]

        output_['muCHG'] = Q_at_MK_[1]
        output_['loCHG'] = Q_at_LW_[1]
        output_['maCHG'] = list(map(float,Q_at_MY_['QA   - Mulliken gross atomic charge']))
        
        output_['vF'] = F 
        #output_['F_X'] = F[0]
        #output_['F_Y'] = F[1]
        #output_['F_Z'] = F[2]
        #print(output_)
        output_['eAT'] = round(E_AT,6)
        output_['Gcmbdf'] = list(GEO)
        #bd.dat 
        if 'bd.dat' in os.listdir():
            output_['eBIND'] = round(E_BD,6)
       
    
        #save into json file
        with open('file.json','w') as fd:
            json.dump(output_,fd,indent=4)

#from lines properties
def coordinates(lines):
    idx1 = lines.index([i for i in lines if 'CARTESIAN COORDINATES (ANGSTROEM)' in i][0]) #search for  1st line
    idx2 = lines.index([i for i in lines if 'CARTESIAN COORDINATES (A.U.)' in i][0])# almost last line
    coord = lines[idx1+2:idx2-2] #to get 1st and lst line
    #_ = [i.split() for i in coord]
    #check nunmber of atoms 
    #num = int(lines[lines.index([i for i in lines if 'Number of atoms' in i][0])].split(' ')[-1]) #get the tot number of atoms
    #if len(coord) != num:
        # print('congrats, atoms number matches')
    #    coord = 'Missing'
    atNUM = []
    atXYZ = []
    string_dt = h5py.string_dtype(encoding='utf-8')
    for ele in coord:
        p_ele = str(ele).strip("b' ").split()
        atNUM.append(p_ele[0]) # element list
        #print(p_ele[0])
        atXYZ.append([float(i) for i in p_ele[1:]])
    
    atNUM=np.array(atNUM,dtype=string_dt)

    # convert atNUM into int
    _ = []
    for ele in atNUM:
        if ele == 'C':
            i = 6
        elif ele == 'O':
            i = 8
        elif ele == 'S':
            i = 16
        elif ele == 'N':
            i = 7
        elif ele == 'H':
            i = 1
        _.append(i)
    
    return _, atXYZ


def total_energy(lines):
    # eV
    idx1 = lines.index([i for i in lines if 'FINAL SINGLE POINT ENERGY' in i][0])
    e_tot = float(lines[idx1].split(' ')[-1])*ha2eV
    return round(e_tot,6)

def energy_components(lines): 
    components = {}
    # eV
    #dispersion
    idx1 = lines.index([i for i in lines if 'Edisp/kcal,au:' in i][0])
    components['Edisp'] = float(lines[idx1].split(' ')[-2]) *ha2eV
    components['E6'] = float(lines[idx1+1].split(' ')[-2]) *kcal2eV
    components['E8'] = float(lines[idx1+2].split(' ')[-2]) *kcal2eV
    #energy components eV
    components['E_TOT_SCF'] =  float(lines[lines.index([i for i in lines if 'Total Energy' in i][0])].split(' ')[-2])
    components['NUR'] = float(lines[lines.index([i for i in lines if 'Nuclear Repulsion  :' in i][0])].split(' ')[-2])
    components['ELE'] = float(lines[lines.index([i for i in lines if 'Electronic Energy  :' in i][0])].split(' ')[-2])
    components['1E'] = float(lines[lines.index([i for i in lines if 'One Electron Energy:' in i][0])].split(' ')[-2])
    components['2E'] = float(lines[lines.index([i for i in lines if 'Two Electron Energy:' in i][0])].split(' ')[-2])
    components['virial_pe'] = float(lines[lines.index([i for i in lines if 'Potential Energy   :' in i][0])].split(' ')[-2])
    components['virial_ke'] = float(lines[lines.index([i for i in lines if 'Kinetic Energy     :' in i][0])].split(' ')[-2])
    #DFT energy components
    components['DFT_X'] = float(lines[lines.index([i for i in lines if 'E(X)' in i][0])].strip(' ').split(' ')[-2]) * ha2eV
    components['DFT_C'] = float(lines[lines.index([i for i in lines if 'E(C)' in i][0])].strip(' ').split(' ')[-2]) * ha2eV
    components['DFT_XC'] = float(lines[lines.index([i for i in lines if 'E(XC)' in i][0])].strip(' ').split(' ')[-2]) * ha2eV

    return components

def Orbital_energy(lines):
    #Orbital_energies = {}
    Orbital_energies = []
    # -10 ~ +10 to 
    idx1 = lines.index([i for i in lines if 'OCC' in i][0]) #search for OCC 1st line
    idx2 = lines.index([i for i in lines if 'MULLIKEN POPULATION ANALYSIS' in i][0])#search for MULLIKEN POPULATION ANALYSIS
    df_ = pd.DataFrame(lines[idx1:idx2-2]) # 1st and last line of orbital energies
    #
    #get separate element in each line
    _ = df_[0].str.split(expand=True)
    header = _.loc[0]
    _ = _[1:]
    _.columns = header
    _ = _.astype(float)
    # get HOMO/LUMO Energies E_gp
    HOMO =  _[_['OCC']==2][header[3]].max() # header[3] is 'E(eV)'
    LUMO =  _[_['OCC']==0][header[3]].min()
    E_gp = LUMO - HOMO # already float number here num = int(lines[lines.index([i for i in lines if 'Number of atoms'
    
    # get - 10 HOMO and + 10 LUMO total 22 orbitals
    idx_HOMO = _[_['E(eV)']==HOMO].index[0]
    #put NO orbital and E(eV) into dictionary
    s = zip(_.loc[idx_HOMO - 10: idx_HOMO + 11 ]['NO'],_.loc[idx_HOMO - 10: idx_HOMO + 11 ]['E(eV)'])
    for i,j in iter(s):
        #Orbital_energies[i] = j
        Orbital_energies.append(j)


    return HOMO, LUMO, E_gp, Orbital_energies

def disp_coef(lines):
    # a.u.
    #unit E_h * a0^6
    idx1 = lines.index([i for i in lines if 'C6(AA)' in i][0])
    C6 = float(lines[idx1].split(' ')[-2])

    return C6


def DP_components(lines):
    DP_components = {}
    #get the components and total DP
    #unit in a.u.
    idx1 = lines.index([i for i in lines if 'DIPOLE MOMENT' in i][0]) # 
    EC = [i for i in lines[idx1+3].split(' ') if i !='']
    DP_components['Electronic contribution X'] = float(EC[-3]) #X
    DP_components['Electronic contribution Y'] = float(EC[-2]) #Y
    DP_components['Electronic contribution Z'] = float(EC[-1]) #Z
    NC = [i for i in lines[idx1+4].split(' ') if i !='']
    DP_components['Nuclear contribution X'] = float(NC[-3]) #X
    DP_components['Nuclear contribution Y'] = float(NC[-2]) #Y
    DP_components['Nuclear contribution Z'] = float(NC[-1]) #Z
    TT = [i for i in lines[idx1+6].split(' ') if i !=''] #Total DP
    DP_components['Total dipole moment contribution X'] = float(TT[-3])
    DP_components['Total dipole moment contribution Y'] = float(TT[-2])
    DP_components['Total dipole moment contribution Z'] = float(TT[-1])
    Dp_tot = float([i for i in lines[idx1+9].split(' ') if i !=''][-1])
    
    return DP_components, Dp_tot

def Rotational_Spectrum(lines):
    #unit in MHz
    Rational_Spectrum = {}
    idx1 = lines.index([i for i in lines if 'Rotational constants in MHz' in i][0])
    Rational_Spectrum['Rational Spectrum X'] = float([i for i in lines[idx1].split(' ') if i != ''][-3])
    Rational_Spectrum['Rational Spectrum Y'] = float([i for i in lines[idx1].split(' ') if i != ''][-2])
    Rational_Spectrum['Rational Spectrum Z'] = float([i for i in lines[idx1].split(' ') if i != ''][-1])
    # dipole moment along rotational axis
    Rational_Spectrum['RS dipole X (Debye)'] = float([i for i in lines[idx1+4].split(' ') if i != ''][-3])
    Rational_Spectrum['RS dipole Y (Debye)'] = float([i for i in lines[idx1+4].split(' ') if i != ''][-2])
    Rational_Spectrum['RS dipole Z (Debye)'] = float([i for i in lines[idx1+4].split(' ') if i != ''][-1])

    return Rational_Spectrum

def QP_components(lines):
    #unit in Buckingham
    QP_components = {}
    idx1 = lines.index([i for i in lines if 'QUADRUPOLE MOMENT (A.U.)' in i][0])
    #NUC
    QP_components['Nuclear contribution XX'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][1])
    QP_components['Nuclear contribution YY'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][2])
    QP_components['Nuclear contribution ZZ'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][3])
    QP_components['Nuclear contribution XY'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][4])
    QP_components['Nuclear contribution XZ'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][5])
    QP_components['Nuclear contribution YZ'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][6])
    #ELC
    QP_components['Electronic contribution XX'] = float([i for i in lines[idx1+5].split(' ') if i!= ''][1])
    QP_components['Electronic contribution YY'] = float([i for i in lines[idx1+5].split(' ') if i!= ''][2])
    QP_components['Electronic contribution ZZ'] = float([i for i in lines[idx1+5].split(' ') if i!= ''][3])
    QP_components['Electronic contribution XY'] = float([i for i in lines[idx1+5].split(' ') if i!= ''][4])
    QP_components['Electronic contribution XZ'] = float([i for i in lines[idx1+5].split(' ') if i!= ''][5])
    QP_components['Electronic contribution YZ'] = float([i for i in lines[idx1+5].split(' ') if i!= ''][6])
    #for Tot in Buckingham
    QP_components['Total quadrupole moment XX'] = float([i for i in lines[idx1+7].split(' ') if i!= ''][0])
    QP_components['Total quadrupole moment YY'] = float([i for i in lines[idx1+7].split(' ') if i!= ''][1])
    QP_components['Total quadrupole moment ZZ'] = float([i for i in lines[idx1+7].split(' ') if i!= ''][2])
    QP_components['Total quadrupole moment XY'] = float([i for i in lines[idx1+7].split(' ') if i!= ''][3])
    QP_components['Total quadrupole moment XZ'] = float([i for i in lines[idx1+7].split(' ') if i!= ''][4])
    QP_components['Total quadrupole moment YZ'] = float([i for i in lines[idx1+7].split(' ') if i!= ''][5])

    return QP_components

def QP_tot(lines): 
    #unit in Buckingham
    idx1 = lines.index([i for i in lines if 'Isotropic quadrupole' in i][0])
    QP_tot = float([i for i in lines[idx1].split(' ') if i != ''][-1])
    return QP_tot

def PA_tensor(lines):
    #unit in a.u.
    PA_tensor = {}
    idx1 = lines.index([i for i in lines if 'THE POLARIZABILITY TENSOR' in i][0])
    PA_tensor['POLARIZABILITY TENSOR XX'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][0])
    PA_tensor['POLARIZABILITY TENSOR YY'] = float([i for i in lines[idx1+5].split(' ') if i!= ''][1])
    PA_tensor['POLARIZABILITY TENSOR ZZ'] = float([i for i in lines[idx1+6].split(' ') if i!= ''][2])
    PA_tensor['POLARIZABILITY TENSOR XY'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][1])
    PA_tensor['POLARIZABILITY TENSOR XZ'] = float([i for i in lines[idx1+4].split(' ') if i!= ''][2])
    PA_tensor['POLARIZABILITY TENSOR YZ'] = float([i for i in lines[idx1+5].split(' ') if i!= ''][2])
    return PA_tensor

def Iso_PA(lines):
    #unit in a.u.
    idx1 = lines.index([i for i in lines if 'Isotropic polarizability' in i][0])
    Iso_PA = float(lines[idx1].split(' ')[-1])
    return Iso_PA

#structural


def Rg():
    xyz_file=[geo for geo in os.listdir() if '.xyz' in geo][0]
    Rg = get_rg(xyz_file)
    #print(Rg)
    return Rg

def Im():
    xyz_file=[geo for geo in os.listdir() if '.xyz' in geo][0]
    '''
    Tensor: xx,yy,zz,xy,xz,yz
    '''
    Im = get_inertia_tensor(xyz_file)
    return Im


#atomic properties

def Q_at_MK(lines): 
    #get Mulliken charge population
    q = {}
    idx1 = lines.index([i for i in lines if 'MULLIKEN ATOMIC CHARGES' in i][0])
    idx2 = lines.index([i for i in lines if 'Sum of atomic charges:' in i][0])
    _ = lines[idx1 + 2 : idx2]
    __ =[]
    for i in _:
        q_ = [i for i in i.split(' ') if i != '']
        q[f'{q_[0]}{q_[1]}'] = float(q_[-1])
        __.append(float(q_[-1]))
    return q, __

def Q_at_LW(lines):
    #get lowdin charges
    q = {}
    idx1 = lines.index([i for i in lines if 'LOEWDIN ATOMIC CHARGES' in i][0])
    idx2 = lines.index([i for i in lines if 'LOEWDIN REDUCED ORBITAL CHARGES' in i][0])
    _ = lines[idx1 + 2 : idx2-2]
    __ = []
    for i in _:
        q_ = [i for i in i.split(' ') if i != '']
        q[f'{q_[0]}{q_[1]}'] = float(q_[-1])
        __.append(float(q_[-1]))
    return q, __

def Q_at_MY(lines):
    q = {}
    #get MY population
    idx1 = lines.index([i for i in lines if "Mayer's free valence" in i][0])
    idx2 = lines.index([i for i in lines if "Mayer bond orders larger than" in i][0])
    _ = lines[idx1 + 2: idx2 -1]
    __ = [i.split() for i in _]
    df_ = pd.DataFrame(__[1:])

    df_ = df_.drop([0],axis=1) # drop the index line
    Note = ['Atom','NA   - Mulliken gross atomic population','ZA   - Total nuclear charge','QA   - Mulliken gross atomic charge',"VA   - Mayer's total valence","BVA  - Mayer's bonded valence","FA   - Mayer's free valence"]
    df_.columns = Note
    #assgin value to dictionary
    for i in df_.columns:
        q[i] = list(df_[i].values)
    return q

def F_atm(lines):
    idx1 = lines.index([i for i in lines if "CARTESIAN GRADIENT" in i][0])
    idx2 = lines.index([i for i in lines if "Difference to translation invariance:" in i][0])
    _ = lines[idx1 + 3: idx2 - 1]
    s = [i.split() for i in _]
    F_X = []
    F_Y = []
    F_Z = []
    for i in range(0,len(s)):
        F_X.append(round(-float(s[i][3]),6))
        F_Y.append(round(-float(s[i][4]),6))
        F_Z.append(round(-float(s[i][5]),6))
    F_output = np.transpose([F_X,F_Y,F_Z]).tolist() # list() only works for the outermost layer
    #print(type(F_output))
    #_ = [round(num,6) for num in F_output]
    return F_output

#def get_cmbdf():
#    #
#    cmbdf = np.loadtxt('./cmbdf.dat')
#    return cmbdf


def E_bd():
    # add bd.dat into file.json 
    # only if bd.dat exist
    if 'bd.dat' in os.listdir():
        E_BD = float(np.loadtxt('./bd.dat'))
        return E_BD

    else:
        pass


def main(output): 
    get_data(output)

if __name__ == "__main__":
    main('output')
