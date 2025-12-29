#!/usr/bin/env python3

import h5py
import pandas as pd
from tqdm import tqdm
import numpy as np
import argparse
from joblib import dump, load

#MORE-Q-G1
def get_OM_df(path='./MORE_Q_G1.hdf5'):
    with h5py.File(path,'r') as f:
        #df_ = f['/']['OM']['01_om']
        xx_om = list(f['/']['OM'].keys())[0] #stands for 01_om
        df = pd.DataFrame(columns=f['/']['OM'][xx_om].keys(),index=f['/']['OM'].keys())
        #give props to df
        for om in tqdm(list(f['/']['OM'].keys())):
            for prop in f['/']['OM'][f'{om}'].keys():
                #df [col] [row]  
                df.loc[f'{om}',f'{prop}'] = f['/']['OM'][f'{om}'][f'{prop}'][...]
        #print(df.shape)
    return df

def get_REC_df(path='./MORE_Q_G1.hdf5'):
    with h5py.File(path,'r') as f:

        xx_rec = list(f['/']['REC'].keys())[0] #stands for 01_om
        df = pd.DataFrame(columns=f['/']['REC'][f'{xx_rec}'].keys(),index=f['/']['REC'].keys())
        #give props to df
        for rec in tqdm(f['/']['REC'].keys()):
            for prop in f['/']['REC'][f'{rec}'].keys():
                #df [col] [row]  
                df.loc[f'{rec}',f'{prop}'] = f['/']['REC'][f'{rec}'][f'{prop}'][...]
        #print(df.shape)
    return df

#MORE-Q-G2
def get_XTB_df(path='./MORE_Q_G2.hdf5',sys='REC'): 
    with h5py.File(path,'r') as f:
        data = []
        xx_recs = list(f['/']['XTB'].keys()) #stands for xx_rec
        xx_oms = list(f['/']['XTB'][f'{xx_recs[0]}'].keys()) # stands for all om index
        #xx_dms = list(f['/']['xTB'][f'{xx_recs[0]}'][f'{xx_oms[0]}'].keys())[0]
        xx_props = list(f['/']['XTB'][f'{xx_recs[0]}'][f'{xx_oms[0]}']['0_dm'][sys].keys()) # take just 01_rec 01_om 01_dm 'REC' system as example
        for xx_rec in tqdm(xx_recs):
            for xx_om in xx_oms:
                for xx_dm in list(f['/']['XTB'][xx_rec][xx_om].keys()):
                    _data = []
                    for xx_prop in xx_props:
                        _data.append(f['/']['XTB'][xx_rec][xx_om][xx_dm][sys][xx_prop][...])
                    data.append([int(xx_rec.split('_')[0]),int(xx_om.split('_')[0]),int(xx_dm.split('_')[0])] + _data)
        df = pd.DataFrame(data,columns=['REC','OM','DM'] + xx_props)
    return df

def get_XTB_ORCA_df(path='./MORE_Q_G2.hdf5',sys='REC'): 
    with h5py.File(path,'r') as f:
        data = []
        xx_recs = list(f['/']['ORCA'].keys()) #stands for xx_rec
        xx_oms = list(f['/']['ORCA'][f'{xx_recs[0]}'].keys()) # stands for all om index
        #xx_dms = list(f['/']['XTB'][f'{xx_recs[0]}'][f'{xx_oms[0]}'].keys())[0]
        xx_props = list(f['/']['ORCA'][f'{xx_recs[0]}'][f'{xx_oms[0]}']['0_dm'][sys].keys()) # take just 01_rec 01_om 01_dm 'REC' system as example
        for xx_rec in tqdm(xx_recs):
            for xx_om in xx_oms:
                for xx_dm in list(f['/']['ORCA'][xx_rec][xx_om].keys()):
                    _data = []
                    for xx_prop in xx_props:
                        _data.append(f['/']['ORCA'][xx_rec][xx_om][xx_dm][sys][xx_prop][...])
                    data.append([int(xx_rec.split('_')[0]),int(xx_om.split('_')[0]),int(xx_dm.split('_')[0])] + _data)
        df = pd.DataFrame(data,columns=['REC','OM','DM'] + xx_props)
    return df 

#MORE-Q-G3
def get_VASP_df(path='./MORE_Q_G3.hdf5',sys='CPLX'):
    with h5py.File(path,'r') as f:
        
        xx_recs = list(f['/'][sys].keys()) #stands for xx_rec
        xx_oms = list(f['/'][sys][f'{xx_recs[0]}'].keys()) # stands for all om index
        props = list(f['/'][sys][f'{xx_recs[0]}'][f'{xx_oms[0]}']['0_dm'].keys()) # stands for all properties index
        #print(props)
        df = pd.DataFrame(columns=list(['REC','OM','DM'] + props),index=range(1,1837)) #total range should be user defined
        
        #assgin xx_rec & xx_om to df
        REC_ = np.repeat(np.arange(1, len(xx_recs)+1), 102) #very useful tool 
        OM_ = np.tile(np.arange(1, len(xx_oms)+1), 18) # very useful tool
        
        df['REC'] = REC_
        df['OM'] = OM_
        #df
        #assign props to df
        m,n = 1,1
        for prop in tqdm(props):
            m = 1
            for xx_rec in xx_recs:
                n =1
                for xx_om in xx_oms:
                    #print(type(f['/']['CPLX'][f'{xx_rec}'][f'{xx_om}'][f'{prop}'][...]))
                    #print(df[(df['REC'] == m) & (df['OM'] == n)].index[0])
                    idx = df[(df['REC'] == m) & (df['OM'] == n)].index[0]
                    
                    dm = list(f['/'][sys][f'{xx_rec}'][f'{xx_om}'].keys())[0]
                    df.at[idx,'DM']=int(dm.split('_')[0])
                    value = f['/'][sys][f'{xx_rec}'][f'{xx_om}'][f'{dm}'][f'{prop}'][...]
                    df.at[idx,prop] = value
                    n +=1
                m += 1
        #print(df.shape)
    return df

def save_df_joblib(df,filename):
    dump(df,filename,compress=3)

#def load_df_joblib(filename):
#    df_loaded = load(filename)
    

def main(ds):
    
    if ds in ['G1_OM','G1_REC','G2_XTB_OM','G2_XTB_REC','G2_XTB_DM','G2_XTB_ORCA_OM', 
          'G2_XTB_ORCA_REC',
          'G2_XTB_ORCA_DM',
          'G3_VASP_CPLX',
          'G3_VASP_OM',
          'G3_VASP_SUB','G3_VASP_BD']:
        if ds == 'G1_OM':
            print('G1_OM will be output')
            DF = get_OM_df()
        elif ds == 'G1_REC':
            print('G1_REC will be output')
            DF = get_REC_df()
        elif ds == 'G2_XTB_REC':
            print('G2_XTB_REC will be output')
            DF = get_XTB_df(sys='REC')
        elif ds == 'G2_XTB_OM':
            print('G2_XTB_OM will be output')
            DF = get_XTB_df(sys='OM')
        elif ds == 'G2_XTB_DM':
            print('G2_XTB_DM will be output')
            DF = get_XTB_df(sys='DM')
        elif ds == 'G2_XTB_ORCA_OM':
            print('G2_XTB_ORCA_OM will be output')
            DF = get_XTB_ORCA_df(sys='OM')
        elif ds == 'G2_XTB_ORCA_REC':
            print('G2_XRB_ORCA_REC will be output')
            DF = get_XTB_ORCA_df(sys='REC')
        elif ds == 'G2_XTB_ORCA_DM':
            print('G2_XRB_ORCA_DM will be output')
            DF = get_XTB_ORCA_df(sys='DM')
        elif ds == 'G3_VASP_CPLX':
            print('G3_VASP_CPLX will be output')
            DF = get_VASP_df(sys='CPLX')
        elif ds == 'G3_VASP_OM':
            print('G3_VASP_OM will be output')
            DF = get_VASP_df(sys='OM')
        elif ds == 'G3_VASP_SUB':
            print('G3_VASP_SUB will be output')
            DF = get_VASP_df(sys='SUB')       
        elif ds == 'G3_VASP_BD':
            print('G3_VASP_BD will be printed')
            DF = get_VASP_df(sys='BD')

    elif ds == 'all':

        print('All subsets will be printed')
        DF = get_OM_df()
        #DF.to_csv('G1_OM')
        save_df_joblib(DF,filename='G1_OM.joblib')
        print('G1_OM printed')

        DF = get_REC_df()
        #DF.to_csv('G1_REC.csv')
        save_df_joblib(DF,filename='G1_REC.joblib')
        print('G1_REC printed')

        DF = get_XTB_df(sys='REC')
        #DF.to_csv('G2_XTB_REC.csv')
        save_df_joblib(DF,filename='G2_XTB_REC.joblib')
        print('G2_XTB_REC printed')
        
        DF = get_XTB_df(sys='OM')
        #DF.to_csv('G2_XTB_OM.csv')
        save_df_joblib(DF,filename='G2_XTB_OM.joblib')
        print('G2_XTB_OM printed')

        DF = get_XTB_df(sys='DM')
        #DF.to_csv('G2_XTB_DM.csv')
        save_df_joblib(DF,filename='G2_XTB_DM.joblib')
        print('G2_XTB_DM printed')

        DF = get_XTB_ORCA_df(sys='OM') 
        #DF.to_csv('G2_XTB_ORCA_OM.csv')
        save_df_joblib(DF,filename='G2_XTB_ORCA_OM.joblib')
        print('G2_XTB_ORCA_OM printed')

        DF = get_XTB_ORCA_df(sys='REC')
        #DF.to_csv('G2_XTB_ORCA_REC.csv')
        save_df_joblib(DF,filename='G2_XTB_ORCA_REC.joblib')
        print('G2_XTB_ORCA_REC printed')

        DF = get_XTB_ORCA_df(sys='DM')
        #DF.to_csv('G2_XTB_ORCA_DM.csv')
        save_df_joblib(DF,filename='G2_XTB_ORCA_DM.joblib')
        print('G2_XRB_ORCA_DM printed')
       
        DF = get_VASP_df(sys='CPLX')
        #DF.to_csv('G3_VASP_CPLX.csv')
        save_df_joblib(DF,filename='G3_VASP_CPLX.joblib')
        print('G3_VASP_CPLX printed')

        DF = get_VASP_df(sys='OM')
        #DF.to_csv('G3_VASP_OM.csv')
        save_df_joblib(DF,filename='G3_VASP_OM.joblib')
        print('G3_VASP_OM printed')

        DF = get_VASP_df(sys='SUB')
        save_df_joblib(DF,filename='G3_VASP_SUB.joblib')
        print('G3_VASP_SUB printed')

        DF = get_VASP_df(sys='BD')
        save_df_joblib(DF,filename='G3_VASP_BD.joblib')
        print('G3_VASP_BD printed')
        print('All subsets printed')
        
    else:
        DF = None
        print('Please type the correct name. No output will be made')
        
    return DF

if __name__ == "__main__":
    #DF = None
    parser = argparse.ArgumentParser(description='to obtain dataset')
    parser.add_argument('-ds',type=str,help="Type anyone of the following: 'G1_OM', 'G2_REC', 'G2_XTB_OM', 'G2_XTB_REC', 'G2_XTB_DM', 'G2_XTB_ORCA_OM', 'G2_XTB_ORCA_REC', 'G2_XTB_ORCA_DM', 'G3_VASP_CPLX', 'G3_VASP_OM', 'G3_VASP_SUB', or type 'all' to produce all the DF files")
    args = parser.parse_args()
    # Defualt 
    #allocate to Dataset
    ds = args.ds
    if ds == 'all':
        main(ds)
    else: 
        DF_target = main(ds)
        dump(DF_target,f'{ds}.joblib',compress=3)


    
    
