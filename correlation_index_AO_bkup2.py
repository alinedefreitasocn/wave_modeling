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

# clevs = np.arange(-1, 1.1, 0.1)
clevs = np.linspace(-1, 1, 21)
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
                                dim='time').to_dataset(name='Mwd')
                        ]
                    )

# saving correlation matrix as file
correlacao.to_netcdf(path=(finalpath + 'map_corr2_' + tele + '.nc'))

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


