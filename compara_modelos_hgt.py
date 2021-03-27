#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 11:09:40 2021

@author: aline

Comparing geopotential from ERA and from the future model 

READING HISTORICAL GEOPOTENTIAL DATA FROM MARIANAS MODEL
ESPATIAL RESOLUTION OF 1.125
ERA 5 has a resolution of 0.25

Resampling historical model to compare with ERA5
"""
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.cm as cm
import numpy as np
import cfgrib
from cfgrib import xarray_store

" Historical hgt from Marianas model CMIP5"
mypath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'
historical = xr.open_dataset(mypath + 'Historical_concat_1960_2100(1).nc')
historical = historical.sel(time=slice('1960-01-01', '2020-08-01'))


" ERA5 geopotential "
dataDIR = '/home/aline/Documents/Dados/ERA5/geopotential_1979_2020.grib'

DS = cfgrib.open_datasets(dataDIR)[0]
DS = DS.assign(hgt = DS.z / 9.81)
DS = DS.assign(hgt_mean = DS.hgt.mean(axis=0))
DS = DS.assign(hgt_anomalie = DS.hgt - DS.hgt_mean)

# separando soh o HGT para ficar mais leve o calculo
hgt = DS['hgt'].to_dataset()

solver, eof1, var1 = calcEOF(hgt, 'hgt', 'latitude')



plt.figure()
historical.hgt.sel(lat=40, lon=5, method='nearest').plot(label='historical',
                                                         color='DarkBlue',
                                                         linestyle='--')
f.hgt.sel(lat=40, lon=5, method='nearest').plot(label='ERA5', 
                                                color= 'DarkRed',
                                                linestyle=':')
plt.legend()
plt.grid(':')

# statistical
hist_mean = historical.hgt.mean(dim='time')
f_mean = f.hgt.mean(dim='time')
diff_mean = f_mean - hist_mean


proj = ccrs.Orthographic(0, 90)
# ax = plt.axes(projection=proj)
plt.figure()
ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
f_mean.plot.contourf(levels = np.linspace(0, 200, 10),
                            cmap=plt.cm.Oranges,
                         transform=ccrs.PlateCarree()
                         )
plt.title('ERA5 time mean')

plt.figure()
ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
hist_mean.plot.contourf(levels = np.linspace(0, 200, 10),
                            cmap=plt.cm.Oranges,
                         transform=ccrs.PlateCarree()
                         )
plt.title('Historical model time mean')

plt.figure()
ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
diff_mean.plot.contourf(levels = np.linspace(0, 200, 10),
                            cmap=plt.cm.Oranges,
                         transform=ccrs.PlateCarree()
                         )
plt.title('Differences in time mean')
