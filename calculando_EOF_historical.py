#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 09:44:31 2021

@author: aline

quero comparar os indices do NCEP e do historical e fazer uma analise 
temporal da variacao dos indices

"""
import xarray as xr
from eofs.xarray import Eof
from calculaEOF import calcEOF
from reading_AO_index import read_index
import matplotlib.pyplot as plt
import pandas as pd

#####################################################################
####################################################################
# espatial resolution of 1.125
mypath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'

historical = xr.open_dataset(mypath + 'Historical_concat_1960_2100(1).nc')

solver, eof1, var1 = calcEOF(historical, 'hgt', 'lat', centered=False)
eof1_norm = ((eof1.sel(mode=0) * (-1)) /
            eof1.sel(mode=0).std())


hgt = historical - historical.hgt.mean(dim='time')
hgt = hgt.groupby('time.month') - hgt.hgt.groupby('time.month').mean()
pseudo_pcs = solver.projectField(hgt.hgt) /solver.pcs(npcs=1).std()

pseudo_pcs.sel(mode=0).to_netcdf(mypath + 'index_historical1.nc')

clevs = np.linspace(-2, 2, 12)
proj = ccrs.Orthographic(0, 90)
# ax = plt.axes(projection=proj)
plt.figure()
ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
eof1_norm.plot.contourf(
                          levels=clevs,
                            cmap=plt.cm.RdBu_r,
                         transform=ccrs.PlateCarree()
                         )
ax.set_title('EOF1 expressed as covariance ' + str(round(var1.values*100, 2)) + '%', fontsize=16)



f_ind = read_index()
pseudo_pcs.sel(mode=0).plot(linewidth=1,
                            linestyle='--',
                            color='DarkRed',
                            label='Calculated Index - historical')
plt.legend()
plt.xlim(['01-01-1989', '01-01-2020'])
plt.ylabel('AO Index')
plt.draw()



