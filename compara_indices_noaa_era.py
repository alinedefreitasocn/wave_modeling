#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 08:51:23 2021

@author: aline

Calculate stats to compare NOAA and ERA5 indices time series
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error as rmse


fNOAA = '/home/aline/Dropbox/IST_investigation/Teleconnections/AO_index.txt'
fERA = '/home/aline/Documents/Dados/ERA5/index_era5.txt'

noaa = pd.read_csv(fNOAA, sep='\s+',
                names=['year', 'month', 'iNOAA'],
                header=2,
                parse_dates={'datetime':[0, 1]},
                index_col='datetime'
                )

era = pd.read_csv(fERA, 
                  header=0,
                  parse_dates=True,
                  index_col='datetime',
                  names=['datetime', 'iERA'])

# selecting the same time slice
noaa = noaa['1979-01-01':'2020-12-01']

indices = pd.merge(noaa, era, 
                   left_index=True, 
                   right_index=True)

describe = indices.describe()

stats = {
         'mean': indices.mean(),
         'std': indices.std(),
         'pearson':indices.corr(method='pearson'),
         'RMSE': rmse(indices.iNOAA, indices.iERA),
         'bias': sum(indices.iNOAA - indices.iERA)/len(indices),
         'variance': indices.var()
         }


sns.regplot('iERA', 'iNOAA', 
            data=indices, 
            scatter=True,
            fit_reg=True,
            ci=95,
            color='darkslateblue')
