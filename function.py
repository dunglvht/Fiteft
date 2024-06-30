import numpy as np
import pandas as pd
import os
import re
path =  os.path.dirname(os.path.realpath(__file__))
from math import prod as product
# temp = '''
# α0 0.153 0.003
# δHW 0.614 0.027
# α1 0.874 0.010
# δHB 2.294 0.033
# α2 0.881 0.019
# δHWB 0.703 0.029
# βHW -0.133 0.012
# δ(HW,HWB) -1.21 0.04
# βHB 0.005 0.005
# δ(HB,HWB) -1.22 0.06
# βHWB 0.120 0.011
# δ(HW,HB) 0.08 0.07
# δ 0.05 0.06
# '''
# acceptance = pd.read_csv(StringIO(temp), sep='\s+', index_col=0, header=None)
acceptance = pd.Series([ 0.153,  0.614,  0.874,  2.294,  0.881,  0.703, -0.133, -1.21 ,
        0.005, -1.22 ,  0.12 ,  0.08 ,  0.05 ],['α0', 'δHW', 'α1', 'δHB', 'α2', 'δHWB', 'βHW', 'δ(HW,HWB)', 'βHB',
       'δ(HB,HWB)', 'βHWB', 'δ(HW,HB)', 'δ'])


def calculate_A(rules={'HW': [0, 0]}, derivative = False):
    allowed =['HW','HWB','HB','cHW','cHWB','cHB']
    if isinstance(rules,dict):
        Cvecs = pd.DataFrame(rules)
    else :
        Cvecs = rules.copy()
    keys = np.intersect1d(allowed,Cvecs.columns)
    # Cvecs =Cvecs[keys]
    keys = [re.sub(r'^c','', i) for i in Cvecs.columns]
    if (keys != Cvecs.columns).any():
        Cvecs = Cvecs.set_axis(keys, axis = 1)
    shape = Cvecs.shape[0]
    # # print(rulesp)
    A = acceptance[acceptance.index.str.contains(
        r'α', regex=True)].T
    A.index = A.index.str[1:]
    B =  acceptance[acceptance.index.str.contains(
        r'β\w', regex=True)].T
    B.index = B.index.str[1:]
    D = acceptance[acceptance.index.str.contains(
        r'δ\w', regex=True)].T
    D.index = D.index.str[1:]
    DD = acceptance[acceptance.index.str.contains(
        r'δ\(\w', regex=True)].T
    DD.index = DD.index.str[2:-1]
    if len(keys) ==0:
        return (np.ones(shape)*(A[0]+A[1]**2/(A[2] + (D * (B)**2).sum() ))).reshape(-1,1,1)

    if not derivative:
        return (A['0']+A['1']**2/(A['2'] + sum(D[i] * (Cvecs.get(i,0)+ B[i])**2 for i in ['HW','HB','HWB']) +
                        Cvecs.get('HW', 0)*Cvecs.get('HWB', 0) * DD['HW,HWB'] + \
                        Cvecs.get('HB', 0)*Cvecs.get('HWB', 0) * DD['HB,HWB'] + \
                        Cvecs.get('HW', 0)*Cvecs.get('HB', 0) * DD['HW,HB'] + \
                        acceptance.get(f'δ', 0) *product(Cvecs.get(i,0) for i in ['HW','HB','HWB']) )).to_numpy().reshape(-1,1,1)
    if derivative:
        dF = [(acceptance.get(f'δ', 0)* Cvecs.get('HB', 0) * Cvecs.get('HWB', 0) + 2 * (Cvecs.get('HW', 0) + B['HW'])* D['HW'] + 
                                        Cvecs.get('HB', 0) * DD['HW,HB'] + Cvecs.get('HWB', 0) * DD['HW,HWB']),
              (acceptance.get(f'δ', 0)* Cvecs.get('HW', 0) * Cvecs.get('HWB', 0) + 2 * (Cvecs.get('HB', 0) + B['HB'])* D['HB'] + 
                                        Cvecs.get('HW', 0) * DD['HW,HB'] + Cvecs.get('HWB', 0) * DD['HB,HWB']),
              (acceptance.get(f'δ', 0)* Cvecs.get('HB', 0) * Cvecs.get('HW', 0) +  2 * (Cvecs.get('HWB', 0) + B['HWB'])* D['HWB'] + 
                                        Cvecs.get('HB', 0) * DD['HB,HWB'] + Cvecs.get('HW', 0) * DD['HW,HWB'])]
        dF = np.array(dF).T
        dF = (A['1']**2/(A['2'] + (sum(D[i] * (Cvecs[[i]]* B[i])**2 for Ni,i in enumerate(['HW','HB','HWB']))) +
                        Cvecs.get('HW', 0)*Cvecs.get('HWB', 0) * DD['HW,HWB'] + \
                        Cvecs.get('HB', 0)*Cvecs.get('HWB', 0) * DD['HB,HWB'] + \
                        Cvecs.get('HW', 0)*Cvecs.get('HB', 0) * DD['HW,HB'] + \
                        acceptance.get(f'δ', 0) *Cvecs[['HW','HB','HWB']].prod(axis=1))**2).to_numpy().reshape(-1,1) * dF
        dF = pd.DataFrame(dF, columns = ['HW','HB','HWB'])
        temp = pd.DataFrame(np.zeros(Cvecs.shape), columns = Cvecs.columns)
        temp.update(dF)
        return - temp.to_numpy().reshape(Cvecs.shape[0],1,Cvecs.shape[1])

    
def likelihood(y, yhat, correlation_exp, uncertainty_exp, likelihood_type , correlation_theo=None, uncertainty_theo=None):
    # print(y.shape, yhat.shape, correlation_exp.shape, uncertainty_exp.shape)
    if isinstance(y, pd.DataFrame):
      y = y.to_numpy()
    if isinstance(yhat, pd.DataFrame):
      yhat = yhat.to_numpy()
    if isinstance(correlation_exp, pd.DataFrame):
      correlation_exp = correlation_exp.to_numpy()
    if isinstance(uncertainty_exp, pd.DataFrame):
      uncertainty_exp = uncertainty_exp.abs().to_numpy()
    if isinstance(correlation_theo, pd.DataFrame):
      correlation_theo = correlation_theo.to_numpy()
    if isinstance(uncertainty_theo, pd.DataFrame):
      uncertainty_theo = uncertainty_theo.abs().to_numpy()
    # print(y.shape)
    temp = np.array(y-yhat)
    # return temp
    # temp = np.maximum(np.array(y-yhat)-np.abs(uncertainty_theo[:,:1]),0)+np.minimum(np.array(y-yhat)+np.abs(uncertainty_theo[:,:1]),0)
    def calculate_covariance(uncertainty, correlation,likelihood_type):
        if likelihood_type in ['variable gaussian 0', 'vg0', 0]:
            # Sig = np.sqrt(np.absolute(uncertainty[:, 0:1]*uncertainty[:, 1:2] + (uncertainty[:, 0:1]-uncertainty[:, 1:2])*temp)).T
            Sig = np.sqrt(np.abs(uncertainty[:, 0:1]*uncertainty[:, 1:2] + (uncertainty[:, 0:1]-uncertainty[:, 1:2])*temp))
        elif likelihood_type in ['variable gaussian 1', 'vg1', 1]:
            Sig = (2*(uncertainty[:, 0:1]*uncertainty[:, 1:2])/(uncertainty[:, 0:1]+uncertainty[:, 1:2])
             + (uncertainty[:, 0:1]-uncertainty[:, 1:2])/(uncertainty[:, 0:1]+uncertainty[:, 1:2])*temp)
        elif likelihood_type in ['normal gaussian', 'ng', 2]:
            Sig = ((uncertainty[:, 0:1]+uncertainty[:, 1:2])/2)
            return (Sig.dot(Sig.T))*correlation
        else: 
            print(f'unknown likelihood_type {likelihood_type}')
            # print(Sig)
        
        return np.matmul(Sig,np.transpose(Sig,axes = (0,2,1)))* correlation
    
    covariance = calculate_covariance(uncertainty_exp, correlation_exp,likelihood_type)
    if uncertainty_theo is not None:
        covariance_theo  = calculate_covariance(uncertainty_theo, correlation_theo,likelihood_type)
        if np.isnan(covariance_theo).any():
            print(f'fixed some negative sqrt {(np.isnan(covariance_theo).sum()/covariance_theo.size)*100} %')
            covariance_theo  =   np.nan_to_num(covariance_theo,nan=0)+np.isnan(covariance_theo)*calculate_covariance(uncertainty_theo, correlation_theo,'ng')
        covariance = covariance + covariance_theo
          # + covariance_theo  \
          # * np.heaviside(temp-uncertainty_theo[:,:1],0.5)
    else:
      # print('without theoretical uncertainty')
      pass

    inv = np.linalg.inv(covariance)
    # tempp = temp + uncertainty_theo[:,0:1]
    # tempm = temp - uncertainty_theo[:,0:1]
    # print(Sig)
    return np.matmul(np.matmul(np.transpose(temp,axes = (0,2,1)), inv), temp) \
    # + np.matmul(np.matmul(np.transpose(tempp,axes = (0,2,1)), inv), tempp) \
    # + np.matmul(np.matmul(np.transpose(tempm,axes = (0,2,1)), inv), tempm)