#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 11:38:09 2021

@author: aline

- Creating a new xarray with all sea level pressure files
from jerry
- calculate EOF from sea level pressure, get AO pattern
and the index time series
- Create a new xarray with all wave parameters files
- correlate future wave parameters and index.
"""

import xarray as xr
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from calculaEOF import calcEOF
import cartopy.crs as ccrs
import numpy as np
from reading_AO_index import read_index
import pandas as pd



# sea level pressure está em Pa. Deve passar para hPa e depois
# dividir pela gravidade para obter a altura geopotencial.
# mas isso deve ser feito depois d eunir todos os arquivos

# primeiro reunir os dados historicos num unico arquivo:
mypath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'
# mypath = '/home/aline/Documents/Dados/Jerry/SLP/future/'

files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

slp = xr.open_mfdataset(files,
                      combine='by_coords',
                      parallel=True)
pot = slp.Z.sel(lat = slice(90, 20))
# Passando de Pa para hPa
# slp = slp * 0.01
# calculando a altura geopotencial a partir da pressao 
# (difivido pela gravidade)
# hgt = 8 * (slp - 1000)
hgt = pot/9.81
hgt = hgt.round(2)
# slp = slp.resample(time='M').mean()

hgt = hgt.to_dataset(name='hgt')
# tive que salvar como netcdf pq usando o dash nao funciona o EOFs
hgt.isel(plev=0).to_netcdf(mypath + 'Historical_concat_1960_2100(1).nc')



