#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Aline Lemos de Freitas
8 de setembro de 2020

making first test with ERA5netcdf files

GRIb eh mais leve que netCDF
ao baixar ensembles, arquivo GRIB eh lido como uma lista usando o
cfgrib.open_datasets. estou baixando somente a reanalise para ver
como fica a leitura
como eh uma lista, eh possivel selecionar o item que vai ser um
xarray.dataset e pode usar como se fosse o netCDF.

Baixei um unico arquivo GRIB para todo o oceano
 Atlantico Norte. Quando leio, ele eh uma lista
 mas isso se resolve facilmente criando uma nova
variavel selecionando o primeiro item da lista
"""
import xarray as xr
import netCDF4 as nc
import cfgrib
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cfgrib import xarray_store
from calculaEOF import calcEOF
from reading_AO_index import read_index



# single file
# reading grib file with 1000 hpa geopotential height
dataDIR = '/home/aline/Documents/Dados/ERA5/geopotential_1979_2019.grib'

DS = cfgrib.open_datasets(dataDIR)[0]

# ERA5 gives the geopotential of the 1000 hpa. we need
# to divide by gravity to get the geopotential height
DS = DS.assign(hgt = DS.z / 9.81)
DS = DS.assign(hgt_mean = DS.hgt.mean(axis=0))
DS = DS.assign(hgt_anomalie = DS.hgt - DS.hgt_mean)

timeslice = DS.sel(time=slice("1979-01-01",
                                    "2000-12-31"))
timeslice = timeslice['hgt'].to_dataset()
m_anomalie = ((timeslice.groupby('time.month')) -
      timeslice.hgt.groupby('time.month').mean(dim='time'))

completo = DS['hgt'].to_dataset()
completo_manomalie = ((completo.groupby('time.month')) -
                completo.hgt.groupby('time.month').mean())
# OR multiple files
# mfdataDIR = '/home/aline/Documents/ERA5/*.grib'
# DS = xr.open_mfdataset(mfdataDIR, engine='cfgrib')

# Draw coastlines of the Earth
plt.figure()
ax = plt.axes(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
DS.isel(time=0).z.plot(transform=ccrs.PlateCarree())
plt.title(r'Geopotential ($m^2 . s^{-2}$)')
plt.show(block=False)


plt.figure()
ax = plt.axes(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
DS.isel(time=0).hgt.plot(transform=ccrs.PlateCarree())
plt.title('Geopotential height (m)')
plt.show(block=False)

plt.figure()
ax = plt.axes(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
DS.isel(time=0).hgt_mean.plot(transform=ccrs.PlateCarree(),
                                cmap=plt.cm.OrRd)
plt.title('Mean Geopotential height (m)')
plt.show(block=False)

plt.figure()
ax = plt.axes(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
DS.isel(time=0).hgt_sem_media.plot(transform=ccrs.PlateCarree())
plt.title('Geopotential height (m) - mean removed')
plt.show(block=False)

for t in DS.time.values:

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    DS.sel(time=str(t)).swh.plot(
        # figsize = (12,6),      # We'll make it a bit bigger
        vmin=0, vmax=7
    )
    plt.title("Time = " + str(t))
    plt.savefig(f"/home/aline/Documents/IST_investigation/ERA5/images/Python_Animation/Python_Animation_01_frame_{str(t)}.png")
    plt.close()


# Fazer as animacoes. Essa parte entra na linha de
# comando fora do ambiente python
!ls /home/aline/Documents/ERA5/images/Python_Animation/

!convert /home/aline/Documents/ERA5/images/Python_Animation/Python_Animation_01_frame*png /home/aline/Documents/ERA5/images/Python_Animation/Python_Animation_01.gif
display(HTML("<img src='../images/Python_Animation/Python_Animation_01.gif' />"))

###############################
###############################
###############################
# calculating EOF from ERA5
solver, eof1, var1 = calcEOF(m_anomalie, 'hgt', 'latitude')
eof1 = (eof1.sel(mode=0) * (-1))


pseudo_pcs = ((solver.projectField(completo_manomalie.hgt) * (-1))/
                solver.pcs(npcs=1).std())

# Plot the leading EOF expressed as covariance in the European/Atlantic domain.
clevs = np.linspace(-50, 50, 12)
proj = ccrs.Orthographic(0, 90)
# ax = plt.axes(projection=proj)
plt.figure()
ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
ax.coastlines()
ax.set_global()
eof1.plot.pcolormesh(levels=clevs,
                            cmap=plt.cm.RdBu_r,
                         transform=ccrs.PlateCarree(), add_colorbar=True
                         )

ax.set_title('EOF1 expressed as covariance ' + str(round(var1.values*100, 2)) + '%', fontsize=16)
plt.show(block=False)

plt.figure()
read_index()
pseudo_pcs.sel(mode=0).plot(linewidth=2,
                            linestyle='--',
                            color='k',
                            label='Calculated Index ERA5')
plt.legend()
plt.xlim(['01-01-1989', '01-01-2020'])
plt.ylabel('AO Index')
plt.draw()
