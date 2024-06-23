# Fiteft

Fiteft (**fit** **e**ffective **f**ield **t**heory) is a Python package for calculating approximated likelihood function of Standard Model Effective Field Theory (SMEFT) parameters using experimental data. We also provide a method for calculating best-fit and confident interval of SMEFT parameters  

# Requirements:

* Python 3.10 (or 3.X)
* numpy (preferable newest version)
* pandas (preferable newest version)

Optional, for the minimization of the likelihood functions

* scipy (preferable newest version)

# Usage
## Google colab notebook
We provide a step-by-step intruction via a Google colab notebook. User can run the notebook directly through Google's machine.
1. Open the [Colab notebook](https://colab.research.google.com/drive/1eUgw_YGFu6aDmy9yRLbxbCHCWnoglPDP?usp=sharing)
2. Choose `File> Save a copy in Drive`. Now you can start run the notebook
3. Run the setup cell
![setup](<markdown_pngs/Screenshot from 2024-06-23 19-17-52.png>)
4. Full instruction is in the example section, you can run it cell by cell
![example](<markdown_pngs/Screenshot from 2024-06-23 19-31-00.png>)

## GitHub codespace
We also provide a ready-to-run, line-by-line example via GitHub code space
1. Go to the [repository page](https://github.com/dunglvht/Fiteft)
2. Click `Code> Create codespace on master`
![create codespace](<markdown_pngs/Screenshot from 2024-06-23 19-54-52.png>)
3. Open `example.ipynb` via left pannel which will open a jupyter notebook on VScode on GitHub codespace, you then can run the notebook directly on your browser.
![codespace-jupyter](<markdown_pngs/Screenshot from 2024-06-23 19-58-30.png>)

## Using Python script
In a Python script, you first need to clone the Fiteft project by running this command on your terminal

    git clone https://github.com/dunglvht/Fiteft

then you have to add `Fieft` to `sys.path`, then import `Fiteft, python, pandas`.
```
import sys
sys.path.append('<Fiteft_path>')
import numpy as np
import pandas as pd
import Fiteft
```
Next, create a `fiteft` object:
```
>>> f = Fiteft.fiteft(experiment='ATLAS-CONF-2020-053')
Your input to the likelihood function is a DataFrame with at least one of these colums:
['c(3)Hq', 'c[1]HW-HB-HWB-HDD-uW-uB', 'c[2]HW-HB-HWB-HDD-uW-uB', 'c[3]HW-HB-HWB-HDD-uW-uB', 'c[1]Hu-Hd-Hq(1)', 'c[1]Hl(1)-He', 'c[1]Hl(3)-ll0', 'c[1]HG-uG-uH-top', 'c[2]HG-uG-uH-top', 'c[3]HG-uG-uH-top']
```
Now you can start running the `fiteft.likelihood()` function
```
>>> f.likelihood(pd.DataFrame(np.ones((2,2)), columns = ['c(3)Hq','c[1]Hl(3)-ll0']))
array([[[1803.67453384]],

       [[1803.67453384]]])
``` 
or a shorter version, `fiteft.l()` function
```
>>> f.l(np.array([1,0,0,0,0,0,1,0,0,0]))
array([[[1803.67453384]]])
```
# Documentation

Detailed usage is provided via jupyter notebooks. Full description of the file structures, functions is detailed in `thesis.pdf` file, section 4.
