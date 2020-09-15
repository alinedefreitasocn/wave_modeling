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
dataDIR = '/home/aline/Documents/ERA5/montly_mean_1990_2020.grib'

DS = cfgrib.open_datasets(dataDIR)[0]


# OR multiple files
# mfdataDIR = '/home/aline/Documents/ERA5/*.grib'
# DS = xr.open_mfdataset(mfdataDIR, engine='cfgrib')

# Draw coastlines of the Earth
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
DS.isel(time=0).swh.plot()
plt.show(block=False)
