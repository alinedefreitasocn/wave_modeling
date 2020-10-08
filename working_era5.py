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


# single file
dataDIR = '/home/aline/Documents/IST_investigation/ERA5/montly_mean_1990_2020.grib'

DS = cfgrib.open_datasets(dataDIR)[0]


# OR multiple files
# mfdataDIR = '/home/aline/Documents/ERA5/*.grib'
# DS = xr.open_mfdataset(mfdataDIR, engine='cfgrib')

# Draw coastlines of the Earth
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
DS.isel(time=0).swh.plot()
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
