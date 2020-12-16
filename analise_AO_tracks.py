"""
REading Andressa's files of storm track
Using wave height
"""

import pandas as pd


file = '/home/aline/Documents/Dados/tracks_andressa/TrackPar_1980_2020.txt'

df = pd.read_csv(file,
                 sep=',',
                 index_col='Date',
                 parse_dates = True)
df = df.drop(columns='indice')

# selecionando o periodo dos indices igual ao das storms
# da Andressa
indices_crop = indices.sel(time=slice('1980-01-01',
                                    '2019-12-31'))
# pegando a series de indices lida e transformando em
# Dataframe. nao sei pq salvei em netcdf mas fiquei com preguica
# de ajeitar. e para fazer a correla cao com os tracks precisa
# ser dataframe com dataframe
dfindices = indices_crop.to_dataframe()
dfindices = dfindices.drop(columns=['mode', 'month'])


nstorms = df.year.resample('M').count()
nstorms_norm = (nstorms - nstorms.mean())/nstorms.std()
nstorms_norm = nstorms_norm[nstorms_norm.index.year < 2020]


correlation = nstorms_norm.corr(dfindices)
plt.figure()
