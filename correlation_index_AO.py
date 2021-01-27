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

# general definitions
tele = 'AO'
finalpath = (r'/home/aline/Dropbox/IST_investigation'
                           '/Teleconnections/correlacoes/' + tele + '/')

clevs = np.arange(-1, 1.1, 0.1)
colormap = plt.cm.Spectral


'''
******************************************************************************
******************************************************************************
******************************************************************************

                           READING INDEX
                           
******************************************************************************
******************************************************************************
******************************************************************************
                           
'''

if tele == 'AO':
    '''
    REading index file
    for index as txt
    '''
    findex = '/home/aline/Documents/Dados/indices/calculados/index_era5.txt'
    indices = pd.read_csv(findex, 
                      header=0,
                      parse_dates=True,
                      index_col='time',
                      names=['time', 'id'])
elif tele == 'NAO':
    findex = '/home/aline/Documents/Dados/indices/NAO.txt'
    indices = pd.read_csv(findex, sep='\s+',
                    names=['year', 'month', 'id'],
                    header=2,
                    parse_dates={'time':[0, 1]},
                    index_col='time'
                    )

'''
# for index as nc
'''
# findex = '/home/aline/Documents/Dados/ERA5/index_era5.nc'
# indices = xr.open_dataset(findex)
# # seleciona o periodo disponivel do era5
# indices=indices['__xarray_dataarray_variable__'].rename('indices')
# index_crop = indices.sel(time=slice(dwave.isel(time=0).time.values,
#                                 dwave.isel(time=-1).time.values))




'''
******************************************************************************
******************************************************************************
******************************************************************************

                           WAVE CORRELATION
                           
******************************************************************************
******************************************************************************
******************************************************************************
                           
'''

# reading wave file
fwave = '/home/aline/Documents/Dados/ERA5/montly_mean_1979_2020.grib'
dwave = cfgrib.open_datasets(fwave)[0]


# cropping index time series to match data
index_crop = indices[slice(dwave.isel(time=0).time.values,
                                dwave.isel(time=-1).time.values)]
index_crop = index_crop.id.to_xarray()

# selecting winter season for index data
index_winter = index_crop.sel(time=index_crop['time.season']=='DJF')

'''
# Compute the Pearson correlation coefficient between
# two DataArray objects along a shared dimension
'''
# correlacao = {'Hs': xr.corr(dwave.swh.round(3), 
#                             index_crop.round(3), dim='time'),
#               'Tp': xr.corr(dwave.mwp.round(3), 
#                             index_crop.round(3), dim='time'),
#               'Wave Direction': xr.corr(dwave.mwd.round(3), 
#                                         index_crop.round(3), dim='time')}

correlacao = xr.merge(
                        [
                        xr.corr(dwave.swh.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='Hs'),
                        xr.corr(dwave.mwp.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='Tp'),
                        xr.corr(dwave.mwd.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='mwd')
                        ]
                    )

# saving correlation matrix as file
correlacao.to_netcdf(path=(finalpath + 'map_corr2_' + tele + '.nc'))

# plotting figures

# limites = [-104, 40, 20, 85]
# #clevs = np.linspace(-1, 1, 10)

# proj = ccrs.LambertConformal(central_longitude=-40,
#                             central_latitude=50,
#                             standard_parallels=(20,30),
#                             cutoff=20)
# proj= ccrs.Orthographic(0, 90)


for k in ['Hs', 'Tp', 'mwd']:
    # fig, ax = faz_mapa_corr(proj,
    #                         clevs,
    #                         coords_lim = limites)
    fig, ax = faz_mapa_lambert()
    cf = correlacao[k].plot.contourf(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False
                                )
    fig.colorbar(cf, orientation='horizontal', 
                  pad=0.03, shrink=0.8)
    fig.tight_layout()
    ax.add_feature(cfeature.LAND, 
                   # color='gray',
                   alpha=0.8,
                   zorder=100, 
                   edgecolor='black')
    plt.title(k + '/' + tele + ' correlation')
    # plt.show(block=False)
    fig.savefig((finalpath + k + '_' + tele + '_NA_Lambert.png'))
    plt.close()

# Selecting winter season for wave
dwave_winter = dwave.sel(time=dwave['time.season']=='DJF')

correlacao_winter = xr.merge(
                        [
                        xr.corr(dwave_winter.swh.round(3), 
                                index_winter.round(3), 
                                dim='time').to_dataset(name='Hs'),
                        xr.corr(dwave_winter.mwp.round(3), 
                                index_winter.round(3), 
                                dim='time').to_dataset(name='Tp'),
                        xr.corr(dwave_winter.mwd.round(3), 
                                index_winter.round(3), 
                                dim='time').to_dataset(name='mwd')
                        ]
                    )

# saving winter correlation matrix as file
correlacao_winter.to_netcdf(path=(finalpath + 'map_corr_' + 
                                  tele + '_winter2.nc'))
# correlacao_winter = {'Hs': xr.corr(dwave_winter.swh,
#                                     index_winter, dim='time'),
#               'Tp': xr.corr(dwave_winter.mwp, index_winter, dim='time'),
#               'Wave Direction': xr.corr(dwave_winter.mwd,
#                                         index_winter, dim='time')}
#correlacao_winter = xr.Dataset(correlacao_winter)

for k in ['Hs', 'Tp', 'mwd']:
    fig, ax = faz_mapa_lambert()
    # fig, ax = faz_mapa_corr(proj,
    #                         clevs)#,
    #                         #coords_lim = limites)
    cf = correlacao_winter[k].plot.contourf(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False
                                )
    fig.colorbar(cf, orientation='horizontal', 
                  pad=0.03, shrink=0.8)
    fig.tight_layout()
    ax.add_feature(cfeature.LAND, 
                   # color='gray',
                   alpha=0.8,
                   zorder=100, 
                   edgecolor='black')
    plt.title(k + '/' + tele + ' correlation - Winter (DJF)')
    plt.show(block=False)
    fig.savefig((finalpath + k + '_' +
                tele + '_NA_winter_DJF_Lambert2.png'))
    plt.close()




'''
******************************************************************************
******************************************************************************
******************************************************************************

                           WIND CORRELATION
                           
******************************************************************************
******************************************************************************
******************************************************************************
                           
'''

# reading wind file
fwind = '/home/aline/Documents/Dados/ERA5/wind_monthly_1979_2020.grib'
dwind = cfgrib.open_dataset(fwind)

# for wind
index_crop = indices[slice(dwind.isel(time=0).time.values,
                                dwind.isel(time=-1).time.values)]
index_crop = index_crop.id.to_xarray()

# selecting winter season for index data
index_winter = index_crop.sel(time=index_crop['time.season']=='DJF')

correlacao = xr.merge(
                        [
                        xr.corr(dwind.si10.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='wspd'),
                        xr.corr(dwind.u10.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='U'),
                        xr.corr(dwind.v10.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='V')
                        ]
                    )

correlacao.to_netcdf(path=(finalpath + 'map_corr_wind_' + tele + '.nc'))



# fig, axs = plt.subplots(2,3, 
#                         figsize=(15, 6), 
#                         facecolor='w', 
#                         edgecolor='k',
#                         dpi=400)
# axs = axs.ravel()

for k in ['wspd', 'U', 'V']:
    # fig, ax = faz_mapa_corr(proj,
    #                         clevs,
    #                         coords_lim = limites)
    fig, ax = faz_mapa_lambert()
    cf = correlacao[k].plot.contourf(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False
                                )
    fig.colorbar(cf, orientation='horizontal', 
                  pad=0.03, shrink=0.8)
    fig.tight_layout()
    plt.title(k + '/' + tele + ' correlation')
    ax.add_feature(cfeature.LAND, 
                   # color='gray',
                   alpha=0.8,
                   zorder=100, 
                   edgecolor='black')
    # plt.show(block=False)
    fig.savefig((finalpath + k + '_wind_' + tele + '_NA_Lambert.png'),
                dpi=400)
    plt.close()

# Selecting winter season for wave
dwind_winter = dwind.sel(time=dwind['time.season']=='DJF')

correlacao_winter = xr.merge(
                        [
                        xr.corr(dwind_winter.si10.round(3), 
                                index_winter.round(3), 
                                dim='time').to_dataset(name='wspd'),
                        xr.corr(dwind_winter.u10.round(3), 
                                index_winter.round(3), 
                                dim='time').to_dataset(name='U'),
                        xr.corr(dwind_winter.v10.round(3), 
                                index_winter.round(3), 
                                dim='time').to_dataset(name='V')
                        ]
                    )

# saving winter correlation matrix as file
correlacao_winter.to_netcdf(path=(finalpath + 'map_corr_wind_' + 
                                  tele + '_winter.nc'))
# correlacao_winter = {'Hs': xr.corr(dwave_winter.swh,
#                                     index_winter, dim='time'),
#               'Tp': xr.corr(dwave_winter.mwp, index_winter, dim='time'),
#               'Wave Direction': xr.corr(dwave_winter.mwd,
#                                         index_winter, dim='time')}
#correlacao_winter = xr.Dataset(correlacao_winter)

for k in ['wspd', 'U', 'V']:
    fig, ax = faz_mapa_lambert()
    # fig, ax = faz_mapa_corr(proj,
    #                         clevs)#,
    #                         #coords_lim = limites)
    cf = correlacao_winter[k].plot.contourf(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False
                                )
    fig.colorbar(cf, orientation='horizontal', 
                  pad=0.03, shrink=0.8)
    fig.tight_layout()
    ax.add_feature(cfeature.LAND, 
                   # color='gray',
                   alpha=0.8,
                   zorder=100, 
                   edgecolor='black')
    plt.title(k + '/' + tele + ' correlation - Winter (DJF)')
    plt.show(block=False)
    fig.savefig((finalpath + k + '_' +
                tele + '_wind_NA_winter_DJF_Lambert.png'))
    plt.close()


'''
******************************************************************************
******************************************************************************
******************************************************************************

                           WIND WAVE CORRELATION
                           
******************************************************************************
******************************************************************************
******************************************************************************
                           
'''

# reading wind file
fww = '/home/aline/Documents/Dados/ERA5/wind_wave_monthly_1979_2020.grib'
dww = cfgrib.open_dataset(fww)

# for wind
index_crop = indices[slice(dww.isel(time=0).time.values,
                                dww.isel(time=-1).time.values)]
index_crop = index_crop.id.to_xarray()

# selecting winter season for index data
index_winter = index_crop.sel(time=index_crop['time.season']=='DJF')

correlacao = xr.merge(
                        [
                        xr.corr(dww.mpww.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='MPWW'),
                        xr.corr(dww.shww.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='SHWW')
                        ]
                    )

# correlacao['SHWW'] = correlacao['SHWW'].where(correlacao.SHWW <0.999)

correlacao.to_netcdf(path=(finalpath + 'map_corr_wind_wave_' + tele + '.nc'))



# fig, axs = plt.subplots(2,3, 
#                         figsize=(15, 6), 
#                         facecolor='w', 
#                         edgecolor='k',
#                         dpi=400)
# axs = axs.ravel()

for k in ['MPWW', 'SHWW']:
    # fig, ax = faz_mapa_corr(proj,
    #                         clevs,
    #                         coords_lim = limites)
    fig, ax = faz_mapa_lambert()
    cf = correlacao[k].plot.contourf(#levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False
                                )
    fig.colorbar(cf, orientation='horizontal', 
                  pad=0.03, shrink=0.8)
    fig.tight_layout()
    
    ax.add_feature(cfeature.LAND, 
                   # color='gray',
                   alpha=0.8,
                   zorder=100, 
                   edgecolor='black')
    # plt.show(block=False)
    fig.savefig((finalpath + k + '_wind_wave_' + tele + '_NA_Lambert.png'),
                dpi=400)
    plt.close()

# Selecting winter season for wave
dww_winter = dww.sel(time=dww['time.season']=='DJF')

correlacao_winter = xr.merge(
                        [
                        xr.corr(dww_winter.mpww.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='MPWW'),
                        xr.corr(dww_winter.shww.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='SHWW')
                        ]
                    )

# saving winter correlation matrix as file
correlacao_winter.to_netcdf(path=(finalpath + 'map_corr_wind_wave_' + 
                                  tele + '_winter.nc'))
# correlacao_winter = {'Hs': xr.corr(dwave_winter.swh,
#                                     index_winter, dim='time'),
#               'Tp': xr.corr(dwave_winter.mwp, index_winter, dim='time'),
#               'Wave Direction': xr.corr(dwave_winter.mwd,
#                                         index_winter, dim='time')}
#correlacao_winter = xr.Dataset(correlacao_winter)

for k in ['MPWW', 'SHWW']:
    fig, ax = faz_mapa_lambert()
    # fig, ax = faz_mapa_corr(proj,
    #                         clevs)#,
    #                         #coords_lim = limites)
    cf = correlacao_winter[k].plot.contourf(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False
                                )
    fig.colorbar(cf, orientation='horizontal', 
                  pad=0.03, shrink=0.8)
    fig.tight_layout()
    ax.add_feature(cfeature.LAND, 
                   # color='gray',
                   alpha=0.8,
                   zorder=100, 
                   edgecolor='black')
    plt.title(k + '/' + tele + ' correlation - Winter (DJF)')
    plt.show(block=False)
    fig.savefig((finalpath + k + '_' +
                tele + '_wind_NA_winter_DJF_Lambert.png'))
    plt.close()

