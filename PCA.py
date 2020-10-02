# using scikit-learn PCA to calculate AO index
# following the DataCamp tutorial
# https://www.datacamp.com/community/tutorials/principal-component-analysis-in-python

import sklearn as sk
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.signal
import numpy as np


file = "/home/aline/Documents/Dados/NCEP_NCAR/hgt.mon.mean.nc"

# reading data and selecting level, time and latitude (HN)
f = xr.open_dataset(file)
f = f.sel(level=1000, time=slice("1979-01-01","2000-12-01"),
            lat=slice(90,20))

# removing seasonality
data_detrend = scipy.signal.detrend(f.hgt, axis=0)
f_detrend = xr.DataArray(data_detrend, coords=[f.time, f.lat, f.lon], dims=['time', 'lat', 'lon'])

# comparing detrend signal
ax = plt.subplot()
f.sel(lat=38.7, lon=12, method='nearest').hgt.plot()
f_detrend.sel(lat=38.7, lon=12, method='nearest').plot()

limite = max(abs(f_detrend.max()), abs(f_detrend.min()))

for t in range(len(f_detrend.time)):
    ax1 = plt.subplot(projection=ccrs.Orthographic(0, 90))
    f_detrend.isel(time=t).plot(transform=ccrs.PlateCarree(),
                            subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                            cmap='RdBu_r',
                            vmax=limite,
                            vmin=-limite)
    ax1.coastlines(zorder=3)
    plt.title('1000 hPa Geopotential Height Anomalies: ' +
                str(f_detrend.isel(time=t).time.values)[:7])
    plt.savefig('/home/aline/Dropbox/IST_investigation/Teleconnections/AOIndex/figures/altura_detrend_' + str(f_detrend.isel(time=t).time.values)[:7])
    plt.close()

# scaling values to avoid overrepresented areas
new = []
for l in f_detrend.lat.values:
    # confirmar por qual valor multiplica em cada latitude
    x = f_detrend.sel(lat=l) * np.sqrt(abs(np.cos(l)))
    new.append(x)
combined = xr.concat(new, dim=f_detrend.lat)

ax = plt.subplot()
f.sel(lat=90, lon=12, method='nearest').hgt.plot(label='original')
f_detrend.sel(lat=90, lon=12, method='nearest').plot(label='detrend')
combined.sel(lat=90, lon=12, method='nearest').plot(label='combined')
plt.legend()
