"""
REading Andressa's files of storm track
Using wave height

TODO: Salvar a serie de indices em TXT para ler melhor aqui
"""

import pandas as pd
import numpy as np


file = '/home/aline/Documents/Dados/tracks_andressa/TrackPar_1980_2020.txt'

# alterar este arquivo. O que esta atualmente eh o de indices 
findices = '/home/aline/Dropbox/IST_investigation/Teleconnections/AO_index.txt'
findices= (r'/home/aline/Dropbox/IST_investigation/Teleconnections/AOIndex'
           '/indices/calculados/index_era5.txt')

dstorm = pd.read_csv(file,
                 sep=',',
                 index_col='Date',
                 parse_dates = True)
dstorm = dstorm.drop(columns='indice')

# selecionando o periodo dos indices igual ao das storms
# da Andressa
fi = pd.read_csv(findices, sep=',',
                # names=['year', 'month', 'id'],
                # header=0,
                parse_dates=True,
                index_col='time'
                )

nstorms = dstorm.year.resample('M').count()
# transforming it to the same date as index (first day of month)
# to compare along time with index serie
newdt = pd.DataFrame({'year': nstorms.index.year,
                      'month': nstorms.index.month,
                      'day': np.ones(len(nstorms.index.year), 
                                     dtype='int')})
newdt = pd.to_datetime(newdt)

# newnstorms = nstorms.copy()
nstorms.index = newdt
nstorms = nstorms.to_frame()

indices_crop = fi[nstorms.index[0]:nstorms.index[-1]]


joindf = nstorms.join(indices_crop)


# selecting by season
# winter

winter = joindf[(joindf.index.month == 12) | (joindf.index.month == 1) |
                (joindf.index.month == 2)]

spring = joindf[(joindf.index.month >2) & (joindf.index.month < 6)]
summer = joindf[(joindf.index.month > 5) & (joindf.index.month < 9)]
autumn = joindf[(joindf.index.month > 8) & (joindf.index.month < 12)]

correlation = {'annual': joindf.corr().iloc[0,1],
               'winter': winter.corr().iloc[0,1],
               'spring':spring.corr().iloc[0,1],
               'summer': summer.corr().iloc[0,1],
               'autumn':autumn.corr().iloc[0,1]}










# funciona com xarray mas nao com o pandas...
nstorm_monthly_mean = nstorms.groupby(by=nstorms.index.month).mean()


for i in np.arange(1, 13, 1):
    df = nstorms[nstorms.index.month == i] - nstorm_monthly_mean.year[i]
    df.columns = ['norm']
    
    result = pd.append([nstorms, df], axis=1, join='outer')


nstorms_norm = nstorms_norm.reset_index(drop=True)
indices_crop = indices_crop.reset_index(drop=True)
correlation = indices_crop.corr(nstorms_norm.values, method='pearson')
plt.figure()
