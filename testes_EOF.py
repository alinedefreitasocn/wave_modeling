# Rodadad de testes da EOF AO

import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from eofs.xarray import Eof
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import seaborn as sns

# Leitura do arquivo comum para todos
file = "/home/aline/Documents/Dados/NCEP_NCAR/hgt.mon.mean.nc"

# reading data and selecting level, time and latitude (HN)
fo = xr.open_dataset(file)
# selecao de tempo para calculo do pattern EOF
f = fo.sel(level=1000, time=slice("1979-01-01","2000-12-31"),
            lat=slice(90,20))

# Teste 1: calculando medias mensais
# removing seasonality
# making month means from the whole time series
# seasons = {'summer': 'JJA', 'spring': 'MAM',
#             'winter': 'DJF', 'autumn': 'SON'}
mmean = f.hgt.groupby('time.month').mean()
m_anomalie = f.groupby('time.month') - mmean
