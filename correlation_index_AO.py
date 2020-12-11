" calculando a correlacao entre o indice mensal e os parametros de onda"
import xarray as xr
from cfgrib import xarray_store
import cfgrib
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

findex = '/home/aline/Documents/Dados/ERA5/index_era5.nc'
fwave = '/home/aline/Documents/Dados/ERA5/montly_mean_1990_2020.grib'

dwave = cfgrib.open_datasets(fwave)[0]
index = xr.open_dataset(findex)

index=index['__xarray_dataarray_variable__'].rename('indices')
index_crop = index.sel(time=slice(dwave.isel(time=0).time.values,
                                dwave.isel(time=-1).time.values))

correlacao_hs = xr.corr(dwave.swh, index_crop, dim='time')

lon_w=-75
lon_e=0
lat_s=35
lat_n=65

plt.figure()
proj = ccrs.LambertConformal(central_longitude=-40,
                             central_latitude=50,
                             standard_parallels=(20,30))
ax = plt.subplot(projection=proj)
ax.coastlines()
ax.set_global()
correlacao_hs.plot.pcolormesh(
                            cmap=plt.cm.GnBu,
                         transform=ccrs.PlateCarree(), add_colorbar=True
                         )
ax.set_extent([lon_w, lon_e, lat_s, lat_n], ccrs.PlateCarree())
plt.show(block=False)



ax.set_extent([lon_w, lon_e, lat_s, lat_n], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND,  color='gray', zorder=100, edgecolor='k')
ax.add_feature(cfeature.COASTLINE, zorder=100,  color='k')
ax.add_feature(cfeature.BORDERS, zorder=100,  color='k')
fig.canvas.draw()
xticks = [-80, -60, -40, -20, 0]
yticks = [30, 40, 50, 60, 70]
ax.gridlines(xlocs=xticks, ylocs=yticks)
ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
lambert_xticks(ax, xticks)
lambert_yticks(ax, yticks)
cbar=plt.colorbar(KDEd, format='%.2f', fraction=0.029, pad=0.02)
