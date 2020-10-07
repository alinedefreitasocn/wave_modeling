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


file = "/home/aline/Documents/Dados/NCEP_NCAR/hgt.mon.mean.nc"

# reading data and selecting level, time and latitude (HN)
f = xr.open_dataset(file)
f = f.sel(level=1000, time=slice("1979-01-01","2000-12-01"),
            lat=slice(90,20))

# removing seasonality
# data_detrend = scipy.signal.detrend(f.hgt, axis=0)
# f_detrend = xr.DataArray(data_detrend, coords=[f.time, f.lat, f.lon], dims=['time', 'lat', 'lon'])

# comparing detrend signal
f_anomalie = f - f.mean(dim='time')
ax = plt.subplot()
f.sel(lat=38.7, lon=12, method='nearest').hgt.plot()
f_anomalie.sel(lat=38.7, lon=12, method='nearest').hgt.plot()
plt.show(block=False)

# making month means from the whole time series
mmean = f.hgt.groupby('time.month').mean()
m_anomalie = f.groupby('time.month') - mmean

limite = max(abs(f_anomalie.hgt.max()), abs(f_anomalie.hgt.min()))

ax2 = plt.subplot(projection=ccrs.Orthographic(0, 90))
m_anomalie.isel(time=0).hgt.plot(transform=ccrs.PlateCarree(),
                        subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                        cmap='RdBu_r',
                        vmax=limite,
                        vmin=-limite)

plt.figure()
plt.subplot(projection=ccrs.Orthographic(0, 90))
f_anomalie.isel(time=0).hgt.plot(transform=ccrs.PlateCarree(),
                        subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                        cmap='RdBu_r',
                        vmax=limite,
                        vmin=-limite)


limite = max(abs(f_anomalie.hgt.max()), abs(f_anomalie.hgt.min()))
mlimite = max(abs(m_anomalie.hgt.max()), abs(m_anomalie.hgt.min()))


for t in range(len(f_detrend.time)):
    ax1 = plt.subplot(projection=ccrs.Orthographic(0, 90))
    f_anomalie.isel(time=t).plot(transform=ccrs.PlateCarree(),
                            subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                            cmap='RdBu_r',
                            vmax=limite,
                            vmin=-limite)
    ax1.coastlines(zorder=3)
    plt.title('1000 hPa Geopotential Height: ' +
                str(f_anomalie.isel(time=t).time.values)[:7])
    plt.savefig('/home/aline/Dropbox/IST_investigation/Teleconnections/AOIndex/figures/altura_anomalie_' + str(f_anomalie.isel(time=t).time.values)[:7])
    plt.close()

# making plots of the mensal anomalie, from mensal mean
for t in range(len(m_anomalie.time)):
    ax1 = plt.subplot(projection=ccrs.Orthographic(0, 90))
    m_anomalie.isel(time=t).hgt.plot(transform=ccrs.PlateCarree(),
                            subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                            cmap='RdBu_r',
                            vmax=mlimite,
                            vmin=-mlimite)
    ax1.coastlines(zorder=3)
    plt.title('1000 hPa Geopotential Height: ' +
                str(m_anomalie.isel(time=t).time.values)[:7])
    plt.savefig('/home/aline/Dropbox/IST_investigation/Teleconnections/AOIndex/figures/altura_anomalie_mensal_' + str(m_anomalie.isel(time=t).time.values)[:7])
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
coslat = np.cos(np.deg2rad(m_anomalie.coords['lat'].values)).clip(0., 1.)
# np.newaxis add a dimention to wgts. dont know what ... does
# i think its like a transposed. It took all the objects on a list and
# make a new list with lists inside (each list with only one object)
# just an adjustment of format
wgts = np.sqrt(coslat)[..., np.newaxis]
solver = Eof(m_anomalie.hgt, weights=wgts)

# Retrieve the leading EOF, expressed as the covariance between the leading PC
# time series and the input SLP anomalies at each grid point.
eof1 = solver.eofsAsCovariance(neofs=2)

# Plot the leading EOF expressed as covariance in the European/Atlantic domain.
clevs = np.linspace(-75, 75, 11)
proj = ccrs.Orthographic(0, 90)
ax = plt.axes(projection=proj)
ax.coastlines()
ax.set_global()
eof1.sel(mode=0).plot.contourf(ax=ax, levels=clevs, cmap=plt.cm.RdBu_r,
                         transform=ccrs.PlateCarree(), add_colorbar=True)
ax.set_title('EOF1 expressed as covariance', fontsize=16)
plt.show()

"""
######################################################
# END
#######################################################
"""

# new = []
# for l in f_detrend.lat.values:
#     # confirmar por qual valor multiplica em cada latitude
#     x = f_detrend.sel(lat=l) * np.sqrt(abs(np.cos(l)))
#     new.append(x)
# combined = xr.concat(new, dim=f_detrend.lat)

# Detrending and original data
ax = plt.subplot()
f.sel(lat=20, lon=12, method='nearest').hgt.plot(label='original')
f_detrend.sel(lat=20, lon=12, method='nearest').plot(label='detrend')
combined.sel(lat=20, lon=12, method='nearest').plot(label='combined')
plt.legend()
