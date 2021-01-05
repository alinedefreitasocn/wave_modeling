#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 09:47:51 2021

@author: aline

stats to play with
"""

from statsmodels.tsa.seasonal import seasonal_decompose
from dateutil.parser import parse
import pandas as pd


fERA = '/home/aline/Documents/Dados/ERA5/index_era5.txt'

era = pd.read_csv(fERA, 
                  header=0,
                  parse_dates=True,
                  index_col='datetime',
                  names=['datetime', 'iERA'])

result_add = seasonal_decompose(era['iERA'], model='additive', extrapolate_trend='freq')

result_add.plot()
