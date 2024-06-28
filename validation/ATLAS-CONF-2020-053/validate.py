import sys, os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('../../.')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.optimize import minimize
import scipy
import Fiteft

def calculate_likelihood(exp_name, Npoint = 10, devide = False, save_name = 'fit_linear'):
    a = Fiteft.fiteft(experiment=exp_name)
    bigls = []
    # Npoint = 20
    for likelihood_type in ['variable gaussian 0','variable gaussian 1','normal gaussian']:
        # Set attribute for likelihood function
        a.attribute.update({'likelihood_type' : likelihood_type, 'devide' : devide})
        # Find starting point at the minimum (shared over all coefficients)
        res = minimize(lambda x: a.l(x.reshape(1,-1))[0,0,0] , np.zeros(a.Ndf2.shape[1]), jac = lambda x :a.dl(x.reshape(1,-1),)[0,0], method='BFGS', options ={'gtol':1e-3})
        # Loop over coeffients list (fiteft.C2)
        for Ni,name in enumerate(a.C2):
            ls =[]
            # Set up scanning points
            cs = np.linspace(res.x[Ni] -5* res.hess_inv[Ni,Ni]**0.5,res.x[Ni] + 5 * res.hess_inv[Ni,Ni]**0.5, Npoint)
            # Scan to the right of the minimun, then scan to the left of the minimum
            for vals in [cs[(Npoint//2)::1],cs[(Npoint//2)::-1]]:
                # Set up starting point for the nuisance parameters
                temp = np.delete(res.x.copy(), Ni)
                for val in vals:
                    # Find minimum for the nuisance parameters
                    res2 = minimize(lambda x: a.l_profile(x.reshape(1,-1), loc=Ni, val=val,)[0,0,0], temp, jac = lambda x: a.dl_profile(x.reshape(1,-1), loc=Ni,val=val)[0,0], method='BFGS', options ={'gtol':1e-3})
                    ls.append([likelihood_type, name,val,res2.fun])
                    temp = res2.x.copy()
                ls = ls[::-1]
                bigls.append(ls)
    df = pd.DataFrame(np.concatenate(np.array(bigls), axis=0), columns = ['likelihood_type','name','val','L'])
    df[['val','L']] = df[['val','L']].astype(float)
    df.to_csv(f'{save_name}.csv')
    return df

exp_name = 'ATLAS-CONF-2020-053'
df = calculate_likelihood(exp_name)


# plot the results

# df= pd.read_csv(f'fit_linear.csv', index_col = [0])
fig, axes = plt.subplots(nrows = 5,ncols=2, figsize=(8, 11))
count=0
for name,group in df.groupby('name'):
  ax = axes.flatten()[count]
  count+=1
  temp = pd.read_csv(f'validation_data/{name}.csv', header=0).sort_values('x', axis=0)
  ax.plot(temp['x'],temp[' y'],'--', label=f'{exp_name}')
  for name2, group2 in group.groupby('likelihood_type'):
    ax.plot(group2['val'],group2['L'] - group2['L'].min(), label=name2)
  ax.set_ylabel("$\min_{\overline{\\mathbf{c}'}_i}[\mathcal{L}(c'_i,\overline{\\mathbf{c}'}_i)] - \mathcal{L}(\hat{\\mathbf{c}'})$")
  ax.set_title(name)
  ax.set_yticks([1,3.84], minor=False)
  ax.yaxis.grid(True, which='major')
  ax.set_ylim(0,8)
  handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels,loc=(0.5,0.5),bbox_to_anchor=(0.0, 1.0), ncol=4)
fig.tight_layout()
plt.savefig(f'fit_linear.pdf',bbox_inches='tight')
plt.savefig(f'fit_linear.png',bbox_inches='tight')