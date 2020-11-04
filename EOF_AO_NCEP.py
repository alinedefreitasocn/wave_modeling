# using scikit-learn PCA to calculate AO index
# following the DataCamp tutorial
# https://www.datacamp.com/community/tutorials/principal-component-analysis-in-python

import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from calcula_EOF import calcEOF
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import seaborn as sns


file = "/home/aline/Documents/Dados/NCEP_NCAR/hgt.mon.mean.nc"

# reading data and selecting level, time and latitude (HN)
fo = xr.open_dataset(file)
# selecao de tempo para calculo do pattern EOF
f = fo.sel(level=1000, time=slice("1979-01-01","2000-12-31"),
            lat=slice(90,20))
ff = fo.sel(level=1000, lat=slice(90,20))

# removing seasonality
# making month means from the whole time series
# seasons = {'summer': 'JJA', 'spring': 'MAM',
#             'winter': 'DJF', 'autumn': 'SON'}
mmean = f.hgt.groupby('time.month').mean()
m_anomalie = f.groupby('time.month') - mmean
# selecionando so os meses de inverno
november = m_anomalie.sel(time= m_anomalie['time.month']==11)
march = m_anomalie.sel(time= m_anomalie['time.month']==3)
april = m_anomalie.sel(time= m_anomalie['time.month']==4)
winter = m_anomalie.sel(time=m_anomalie['time.season']=='DJF')
wintertime = xr.concat([november, march, april, winter], dim='time')

spring = m_anomalie.sel(time=m_anomalie['time.season']=='MAM')
summer = m_anomalie.sel(time=m_anomalie['time.season']=='JJA')
autumn = m_anomalie.sel(time=m_anomalie['time.season']=='SON')

# fazendo uma media por season
smean = f.hgt.groupby('time.season').mean()
s_anomalie = f.groupby('time.season') - smean

# removendo a media geral da serie
media = f.hgt.mean(axes=0)
anomalie = f - media

# limite = max(abs(wintertime.hgt.max()), abs(wintertime.hgt.min()))

for t in range(len(m_anomalie.time)):
    ax1 = plt.subplot(projection=ccrs.Orthographic(0, 90))
    m_anomalie.isel(time=t).hgt.plot(transform=ccrs.PlateCarree(),
                            subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                            cmap='RdBu_r',
                            vmax=limite,
                            vmin=-limite)
    ax1.coastlines(zorder=3)
    plt.title('1000 hPa Geopotential Height: ' +
                str(m_anomalie.isel(time=t).time.values)[:7])
    plt.savefig('/home/aline/Dropbox/IST_investigation/Teleconnections/AOIndex/figures/altura_anomalie_mensal' + str(m_anomalie.isel(time=t).time.values)[:7])
    plt.close()

"""
#########################################################
# Using EOF tutorial from
# https://ajdawson.github.io/eofs/latest/examples/nao_xarray.html
#
# Begining
"""
# Create an EOF solver to do the EOF analysis.
# Square-root of cosine of
# latitude weights are applied before the computation of EOFs.
# scaling values to avoid overrepresented areas
# np.clip: Given an interval, values outside the interval are clipped to
# the interval edges. For example, if an interval of [0, 1] is specified,
# values smaller than 0 become 0, and values larger than 1 become 1.
# coslat = np.cos(np.deg2rad(m_anomalie.coords['lat'].values)).clip(0., 1.)
# coslat = np.cos(np.deg2rad(winter.coords['lat'].values)).clip(0., 1.)
xrdata = winter
coslat = np.cos(np.deg2rad(xrdata.coords['lat'].values)).clip(0., 1.)
# np.newaxis add a dimention to wgts. dont know what ... does
# i think its like a transposed. It took all the objects on a list and
# make a new list with lists inside (each list with only one object)
# just an adjustment of format
wgts = np.sqrt(coslat)[..., np.newaxis]
# The EOF analysis is handled by a solver class, and the EOF solution
# is computed when the solver class is created. Method calls are then used
# to retrieve the quantities of interest from the solver class.
# center = False do not remove mean from data
# solver = Eof(m_anomalie.hgt, weights=wgts, center=False)

solver = Eof(xrdata.hgt, weights=wgts, center=False)
# solver = Eof(s_anomalie.hgt, weights=wgts, center=False)
# Retrieve the leading EOF, expressed as the covariance between the leading PC
# time series and the input SLP anomalies at each grid point.
eof1 = solver.eofsAsCovariance()
var1 = solver.varianceFraction().sel(mode=0)

# Plot the leading EOF expressed as covariance in the European/Atlantic domain.
clevs = np.linspace(-75, 75, 20)
proj = ccrs.Orthographic(0, 90)
# ax = plt.axes(projection=proj)
plt.figure()
ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
eof1.sel(mode=0).plot.pcolormesh(levels=clevs,
                                cmap=plt.cm.RdBu_r,
                                transform=ccrs.PlateCarree(central_longitude=0),
                                add_colorbar=True
                         )
ax.set_title('EOF1 expressed as covariance ' +
                str(round(var1.values*100, 2)) + '%', fontsize=16)
plt.show(block=False)


"""
######################################################
Using EOF tutorial from
# END
#######################################################
"""
pseudo_pcs = solver.projectField(m_anomalie.hgt, neofs=1, eofscaling=0)

pseudo_pcs.plot(ax=ax, color='k', linestyle='--')
ax.set(ylabel='AO Index')
plt.show(block=False)
# date_form = DateFormatter("%y-%m")
# ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_major_locator(mdates.YearLocator())
