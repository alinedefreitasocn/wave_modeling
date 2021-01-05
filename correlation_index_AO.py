" calculando a correlacao entre o indice mensal e os parametros de onda"
import xarray as xr
from cfgrib import xarray_store
import cfgrib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import cartopy.crs as ccrs
import numpy as np
from faz_figuras import *


findex = '/home/aline/Documents/Dados/ERA5/index_era5.nc'
fwave = '/home/aline/Documents/Dados/ERA5/montly_mean_1979_2019.grib'

dwave = cfgrib.open_datasets(fwave)[0]
# indices = xr.open_dataset(findex)
indices = pd.read_csv(findex, 
                  header=0,
                  parse_dates=True,
                  index_col='time',
                  names=['time', 'indices'])

# seleciona o periodo disponivel do era5
# indices=indices['__xarray_dataarray_variable__'].rename('indices')
# index_crop = indices.sel(time=slice(dwave.isel(time=0).time.values,
#                                 dwave.isel(time=-1).time.values))
index_crop = indices[slice(dwave.isel(time=0).time.values,
                                dwave.isel(time=-1).time.values)]
index_crop = index_crop.to_xarray()

# Compute the Pearson correlation coefficient between
# two DataArray objects along a shared dimension
correlacao = {'Hs': xr.corr(dwave.swh, index_crop, dim='time'),
              'Tp': xr.corr(dwave.mwp, index_crop, dim='time'),
              'Wave Direction': xr.corr(dwave.mwd, index_crop, dim='time')}
# correlacao = xr.Dataset(correlacao)


limites = [-104, 40, 20, 85]
#clevs = np.linspace(-1, 1, 10)
clevs = np.arange(-1, 1.2, 0.2)
colormap = plt.cm.Spectral
#proj = ccrs.LambertConformal(central_longitude=-40,
#                             central_latitude=50,
#                             standard_parallels=(20,30))
proj= ccrs.Orthographic(0, 90)


for k in correlacao.keys():
    fig, ax = faz_mapa_corr(proj,
                            clevs,
                            coords_lim = limites)
    correlacao[k].plot.contourf(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=True
                                )

    plt.title(k + '/AO correlation')
    plt.show(block=False)
    fig.savefig('/home/aline/Dropbox/IST_investigation/Teleconnections' +
                '/correlacoes/'+ k + '_ao_NA.png')
    plt.close()

" Selecionando o periodo de inverno "
index_winter = index_crop.sel(time=index_crop['time.season']=='DJF')
dwave_winter = dwave.sel(time=dwave['time.season']=='DJF')
correlacao_winter = {'Hs': xr.corr(dwave_winter.swh,
                                    index_winter, dim='time'),
              'Tp': xr.corr(dwave_winter.mwp, index_winter, dim='time'),
              'Wave Direction': xr.corr(dwave_winter.mwd,
                                        index_winter, dim='time')}
#correlacao_winter = xr.Dataset(correlacao_winter)

for k in correlacao_winter.keys():
    fig, ax = faz_mapa_corr(proj,
                            clevs)#,
                            #coords_lim = limites)
    correlacao_winter[k].plot.contourf(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=True
                                )

    plt.title(k + '/AO correlation - Winter (DJF)')
    plt.show(block=False)
    fig.savefig('/home/aline/Dropbox/IST_investigation/Teleconnections' +
                '/correlacoes/'+ k + '_ao_NA_winter_DJF_proj_polar.png')
    plt.close()



###############################################################################

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
