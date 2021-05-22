#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 13:58:59 2021

@author: aline

Analisando rodadas de onda da Marta. WW3 forçado pelo vento 
"""

from os import listdir
from os.path import isfile, join
import xarray as xr

mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Futuro/'
mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Presente/'
# mypath = '/home/aline/Documents/Dados/Jerry/SLP/future/'

files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

wavefile = []
windfile = []
for f in files:
    if 'hs.nc' in f:
        wavefile.append(f)
    elif 'wnd.nc' in f:
        windfile.append(f)

waves = xr.open_mfdataset(wavefile,
                      combine='by_coords',
                      parallel=True)
waves = waves.drop_vars('MAPSTA')
waves= waves.sel(latitude=slice(20,90), longitude= slice(-101,  35))


hs_mean = waves.resample(time='BMS').mean()
hs_mean.to_netcdf(mypath + 'presente_hs_mean_mensal.nc')

hs_max = waves.resample(time='BMS').max()
hs_max.to_netcdf(mypath + 'presente_hs_max_mensal.nc')



