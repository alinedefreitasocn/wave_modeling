" calculando a correlacao entre o indice mensal e os parametros de onda"
import xarray as xr
from cfgrib import xarray_store
import cfgrib
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from faz_figuras import *

findex = '/home/aline/Documents/Dados/ERA5/index_era5.nc'
fwave = '/home/aline/Documents/Dados/ERA5/montly_mean_1990_2020.grib'

dwave = cfgrib.open_datasets(fwave)[0]
index = xr.open_dataset(findex)

index=index['__xarray_dataarray_variable__'].rename('indices')
index_crop = index.sel(time=slice(dwave.isel(time=0).time.values,
                                dwave.isel(time=-1).time.values))

correlacao_hs = xr.corr(dwave.swh, index_crop, dim='time')
correlacao_tp = xr.corr(dwave.mwp, index_crop, dim='time')
correlacao_dir = xr.corr(dwave.mwd, index_crop, dim='time')


limites = [-104, 40, 20, 85]
clevs = np.linspace(-1, 1, 10)
proj = ccrs.LambertConformal(central_longitude=-40, central_latitude=50, \
                                 standard_parallels=(20,30))
#proj= ccrs.Orthographic(0, 90)
faz_mapa_corr(proj, clevs, coords_lim=limites)
correlacao_hs.plot.contourf(levels=clevs,
                            cmap=plt.cm.BrBG,
                         transform=ccrs.PlateCarree(),
                         add_colorbar=True
                         )

plt.title('Hs/AO correlation')
plt.show(block=False)

faz_mapa_corr(proj, clevs, coords_lim=limites)
correlacao_hs.plot.contourf(levels=clevs,
                            cmap=plt.cm.BrBG,
                         transform=ccrs.PlateCarree(),
                         add_colorbar=True
                         )

plt.title('Hs/AO correlation')
plt.show(block=False)

correlacao_tp.plot.contourf(levels=clevs,
                            cmap=plt.cm.BrBG,
                         transform=ccrs.PlateCarree(),
                         add_colorbar=True
                         )
plt.title('Tp/AO correlation')
plt.show(block=False)


plt.figure()
ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
correlacao_dir.plot.contourf(levels=clevs,
                            cmap=plt.cm.BrBG,
                         transform=ccrs.PlateCarree(),
                         add_colorbar=True
                         )
plt.title('Wave Direction/AO correlation')
plt.show(block=False)




proj = ccrs.LambertConformal(central_longitude=-40, central_latitude=50, \
                                 standard_parallels=(20,30))
    ax = fig.add_axes([0,0,1,1], projection=proj)
    KDEd = ax.contour(X, Y, Z,
                transform=ccrs.PlateCarree(), linewidths=(2,),
                levels=levelsC, cmap=plt.cm.Greys)
    ax.set_extent([lon_w, lon_e, lat_s, lat_n], ccrs.PlateCarree())
