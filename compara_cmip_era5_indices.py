#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:14:07 2021

@author: aline

Compara estatistica dos indices no ERA5 e no CMIP5
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

path = '/home/aline/Dropbox/IST_investigation/Teleconnections/Future/futuro_era5/'
iERA = pd.read_csv(path + 'era5_stats_mensal_indice.csv',
                   sep=';')

iCMIP = pd.read_csv(path + 'CMIP_stats_indice.csv',
                    sep=';')


iERA.Max.plot(color='DarkRed', label='Max ERA5')
iCMIP.Max.plot(color='DarkRed', linestyle='--', label = 'Max CMIP5')

iERA.Q99.plot(color='DarkOrange', label='Q99 ERA5')
iCMIP.Q99.plot(color='DarkOrange', linestyle='--', label = 'Q99 CMIP5')

iERA.Q95.plot(color='PaleVioletRed', label='Q95 ERA5')
iCMIP.Q95.plot(color='PaleVioletRed', linestyle='--', label = 'Q95 CMIP5')
plt.xlabel(' ')
plt.grid(':', alpha=0.5)
plt.ylim([0,4.5])
plt.ylabel('Index value')
plt.xticks(ticks=[0,2,4,6,8,10], labels=(['Jan','Mar', 'Mai', 'Jul', 'Sep','Nov']))
plt.autoscale(enable=True, axis='x', tight=True)


iERA.STD.plot(color='lightseagreen', label='STD ERA5')
iCMIP.STD.plot(color='lightseagreen', label='STD CMIP5', linestyle='--')
plt.xlabel(' ')
plt.grid(':', alpha=0.5)
plt.ylim([0,1.7])
plt.ylabel('Std index value')
plt.xticks(ticks=[0,2,4,6,8,10], labels=(['Jan','Mar', 'Mai', 'Jul', 'Sep','Nov']))
plt.autoscale(enable=True, axis='x', tight=True)