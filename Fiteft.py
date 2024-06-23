import os
import sys
# import importlib
# importlib.reload(function)
import pandas as pd
import numpy as np
import function
# import tools
# from os import listdir
# import re
# put CV and CF range here
# print('a')
#import data
path =  os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
# calculation
class fiteft:
    def __init__(self,  experiment='ATLAS-CONF-2020-053') -> None:
        self.experiment = experiment
        self.path = path
        self.dir = f'{self.path}/data/{experiment}/'
        self.obs = pd.read_csv(f'{self.dir}/observable.csv', index_col=[0,1,2,3]).bfill(axis=1)
        if 'central_SM' not in self.obs.columns:
            self.obs['central_SM'] = 1
        self.cor_exp = pd.read_csv(f'{self.dir}/correlation.csv',index_col=[0,1],header =[0,1]).loc[pd.MultiIndex.from_frame(self.obs.index.to_frame()[['production','decay']])]
        self.cor_theo = (pd.read_csv(f'{self.dir}/correlation_theory.csv',index_col=[0,1],header =[0,1]) if os.path.isfile(f'{self.dir}/correlation_theory.csv') else np.identity(self.obs.shape[0]))
        self.param = pd.read_csv(f'{self.dir}/parametrization.csv',index_col=0, header = 0).fillna(0)
        self.rot =  (pd.read_csv(f'{self.dir}/rotate.csv',index_col=0) if os.path.isfile(f'{self.dir}/rotate.csv') else None)
        self.param.loc['none'] = 0
        self.attribute = {'likelihood_type' : 2, 'devide': False}
        Nls = []
        Dls = []
        gr = self.obs.groupby('signature')
        for signature,df in gr:
            if signature in ['CS*BR/(CS_SM*BR_SM)','CS*BR']:
                numerator =  self.param.loc[df.index.get_level_values('production')]
                numerator += self.param.loc[df.index.get_level_values('decay')].to_numpy()
                numerator += self.param.loc[df.index.get_level_values('acceptance')].to_numpy()
                denumerator = self.param.loc[['H->all']*df.shape[0]]
            if signature == 'BR/BR_ZZ':
                numerator =  self.param.loc[df.index.get_level_values('decay')]
                numerator += self.param.loc[df.index.get_level_values('acceptance')].to_numpy()
                denumerator = self.param.loc[['H->ZZ->4l']*df.shape[0]]
            if signature == 'CS*BR_ZZ/BR_ZZSM':
                numerator =  self.param.loc[df.index.get_level_values('production')]
                numerator += self.param.loc[['H->ZZ->4l']].to_numpy()
                numerator += self.param.loc[df.index.get_level_values('acceptance')].to_numpy()
                # numerator = numerator * df[['central']].to_numpy()
                denumerator = self.param.loc[['H->all']*df.shape[0]]
            numerator.index = df.index
            denumerator.index = df.index
            Nls.append(numerator)
            Dls.append(denumerator)
        self.Ndf = pd.concat(Nls,axis=0).loc[self.obs.index]
        self.Ddf = pd.concat(Dls,axis=0).loc[self.obs.index]
        self.Adf = self.Ndf-self.Ddf.to_numpy()
        if self.rot is not None:
            self.Ndf2 = self.Ndf[self.rot.columns].dot(self.rot.T)
            self.Ddf2 = self.Ddf[self.rot.columns].dot(self.rot.T)
            self.Adf2 = self.Ndf2-self.Ddf2.to_numpy()
        else :
            self.Ndf2 = self.Ndf.copy()
            self.Ddf2 = self.Ddf.copy()
            self.Adf2 = self.Adf.copy()
        self.C = self.Ndf.columns.copy()
        self.C2 = self.Ndf2.columns.copy()
        print(f'Your input to the likelihood function is a DataFrame with at least one of these colums:\n{list(self.Ndf2.columns)}')
# A = linearized[mat.columns].dot(mat.T).copy()
# cov = cov_exp + cov_th
    def get_loc(self, loc):
        if isinstance(loc, int):
            return self.Ndf2.columns[loc]
        if isinstance(loc, str):
            return loc
    def likelihood(self, C_df): # DataFrame(n,m)-> Array(n,1,1)
        if self.attribute['devide']:
            y = (self.obs[['central_SM']].to_numpy() * (1 + self.Ndf2[C_df.columns].dot(C_df.T).to_numpy())  / ( 1+ self.Ddf2[C_df.columns].dot(C_df.T).to_numpy()))
            y = y.T.reshape(C_df.shape[0],-1,1)
        else:
            y = self.obs[['central_SM']].to_numpy() *  (1 + self.Adf2[C_df.columns].dot(C_df.T).to_numpy() )
            y = y.T.reshape(C_df.shape[0],-1,1)
        if self.experiment in ['ATLAS-CONF-2020-053']:
            loc = (self.obs.index.get_level_values('decay')=='H->ZZ->4l')
            y[:,loc] = y[:,loc]*function.calculate_A(C_df.dot(self.rot.loc[C_df.columns]))
        return function.likelihood(
            y = y
            ,yhat = self.obs[['central']]
            ,correlation_exp = self.cor_exp
            ,uncertainty_exp = self.obs.loc[:,['+total','-total']]
            ,correlation_theo = (np.identity(self.obs.shape[0]) if '+total_SM' in self.obs.columns else None)
            ,uncertainty_theo = (self.obs[['+total_SM','-total_SM']].abs() if '+total_SM' in self.obs.columns else None)
            ,likelihood_type = self.attribute['likelihood_type']
            )
    def l(self,cvecs): #Array(n,1)|Array(n,)|Array(1,n) -> Array(n,)
        if isinstance(cvecs,np.ndarray):
            C_df = pd.DataFrame(cvecs.reshape(-1,self.Ndf2.shape[1]), columns =  self.Ndf2.columns)
        if isinstance(cvecs,pd.DataFrame):
            C_df = cvecs.copy()
        return self.likelihood(C_df)
    
    def dl(self, cvecs,delta=1.49e-08):# DataFrame(n,m)-> Array(n,m,1)
        if isinstance(cvecs,np.ndarray):
            C_df = pd.DataFrame(cvecs, columns = self.Ndf2.columns)
        if isinstance(cvecs,pd.DataFrame):
            C_df = cvecs
        array = np.tile(C_df,(1,C_df.shape[1])).reshape(-1,C_df.shape[1])
        array = array + np.tile(delta * np.identity(C_df.shape[1]),(C_df.shape[0],1))
        C_df2 = pd.DataFrame(array , columns =C_df.columns)
        l2 = self.likelihood(C_df2).reshape(C_df.shape[0],-1,C_df.shape[1])
        l1 = self.likelihood(C_df)
        return (l2-l1)/delta
        
    def l_profile(self, cvecs, loc, val):
        if isinstance(cvecs,np.ndarray):
            if isinstance(loc,int):
                C_df = pd.DataFrame(np.insert(cvecs, loc, val, axis=1), columns =  self.C2)
            if isinstance(loc,str):
                C_df = pd.DataFrame(np.insert(cvecs, self.C2.get_loc(loc), val, axis=1), columns =  self.C2)
        if isinstance(cvecs,pd.DataFrame):
            C_df = cvecs.copy()
            if isinstance(loc,int):
                C_df[[self.C2[loc]]] = val
            if isinstance(loc,str):
                C_df[[loc]] = val
        return self.likelihood(C_df)
    
    def dl_profile(self, cvecs, loc, val, delta=1.49e-08):
        cvecs2 = np.tile(cvecs,(1,cvecs.shape[1])).reshape(-1,cvecs.shape[1])
        cvecs2 = cvecs2 + np.tile(delta * np.identity(cvecs.shape[1]),(cvecs.shape[0],1))
        if isinstance(cvecs,pd.DataFrame):
            C_df = cvecs.copy()
            C_df2 = pd.DataFrame(cvecs2 , columns =C_df.columns)
            l1 = self.l_profile(C_df, loc, val)
            l2 = self.l_profile(C_df2, loc, val).reshape(C_df.shape[0],-1,C_df.shape[1])
        if isinstance(cvecs,np.ndarray):
            l1 = self.l_profile(cvecs, loc, val)
            l2 = self.l_profile(cvecs2, loc, val).reshape(cvecs.shape[0],-1,cvecs.shape[1])
        return (l2-l1)/delta
    