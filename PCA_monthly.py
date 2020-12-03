# using scikit-learn PCA to calculate AO index
# following the DataCamp tutorial
# https://www.datacamp.com/community/tutorials/principal-component-analysis-in-python

import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from eofs.xarray import Eof
from calculaEOF import calcEOF
from reading_AO_index import read_index

"""
“The NCEP/NCAR reanalysis dataset was employed at a horizontal resolution of (lat,lon)=(2.5°X2.5°) for the period 1979 to 2000. The loading pattern of AO is defined as the first leading mode from the EOF analysis of monthly mean height anomalies at 1000-hPa (NH). Note that year-round monthly mean anomaly data has been used to obtain the loading patterns. Since the AO have the largest variability during the cold sesaon (variance of AO), the loading patterns primarily capture characteristics of the cold season patterns.” - NOAA
"""
file = "/home/aline/Documents/Dados/NCEP_NCAR/hgt.mon.mean.nc"

# reading data and selecting level, time and latitude (HN)
f = xr.open_dataset(file)

"""
“To identify the leading teleconnection patterns in the atmospheric circulation, Emperical Orthogonal Function (EOF) was applied to the monthly mean 1000-hPa height anomalies poleward of 20° latitude for the Northern Hemisphere.” - NOAA
"""
completo = f.sel(level=1000,lat=slice(90,20))
# Just remove the mean from the complete time series to use
# in the end
completo = completo - completo.hgt.mean(dim='time')

timeslice = completo.sel(time=slice("1979-01-01",
                                    "2000-12-31"))
# removing seasonality
# making month means from the whole time series
# mmean = f.hgt.groupby('time.month').mean()
"""“The seasonal cycle has been removed from the monthly mean height field.” """
m_anomalie = (timeslice.groupby('time.month') -
            timeslice.hgt.groupby('time.month').mean())

completo = (completo.groupby('time.month') -
            completo.hgt.groupby('time.month').mean())

"""
#########################################################
# Using EOF tutorial from
# https://ajdawson.github.io/eofs/latest/examples/nao_xarray.html
Criei uma funcao chamada calcEOF para isso
#
# Begining
"""

solver, eof1, var1 = calcEOF(m_anomalie, 'hgt')

eof1_norm = (eof1.sel(mode=0) * (-1))/eof1.sel(mode=0).std()
"""Daily and monthly AO indices are constructed by projecting the daily and monthly mean 1000-hPa  height anomalies onto the leading EOF mode. Both time series are normalized by the standard deviation of the monthly index (1979-2000 base period” - NOAA """
pseudo_pcs = ((solver.projectField(completo.hgt) * (-1))/
                solver.pcs(npcs=1).std())
eof1 = eof1 * (-1)
# Plot the leading EOF expressed as covariance in the European/Atlantic domain.
clevs = np.linspace(-50, 50, 12)
proj = ccrs.Orthographic(0, 90)
# ax = plt.axes(projection=proj)
plt.figure()
ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
eof1.sel(mode=0).plot.pcolormesh(levels=clevs,
                            cmap=plt.cm.RdBu_r,
                         transform=ccrs.PlateCarree(), add_colorbar=True
                         )
ax.set_colorbar(extend='both')
ax.set_title('EOF1 expressed as covariance ' + str(round(var1.values*100, 2)) + '%', fontsize=16)
plt.show(block=False)

"""
######################################################
# END
#######################################################
"""
# pcs = solver.pcs(npcs=1)
# pseudo_pcs = solver.projectField(m_anomalie.hgt, eofscaling=1)
# pseudo_pcs = pseudo_pcs/m_anomalie.hgt.std(axis=0)
read_index()
pseudo_pcs.sel(mode=0).plot(linewidth=1,
                            linestyle='--',
                            color='k',
                            label='Calculated Index')
plt.legend()
plt.xlim(['01-01-1989', '01-01-2020'])
plt.ylabel('AO Index')
plt.draw()

# testing the diferrence between pcs and pseudo_pcs
pcs = solver.pcs(npcs=1)
pseudo_pcs = solver.projectField(m_anomalie.hgt)

plt.figure()
pcs.plot(color='DarkRed',
        label='pcs',
        linestyle='--')
pseudo_pcs.sel(mode=0).plot(linestyle='-.',
                            color='DarkBlue',
                            label='pseudo pcs')
plt.legend()
plt.show(block=False)
