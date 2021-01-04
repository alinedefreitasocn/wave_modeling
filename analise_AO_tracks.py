"""
REading Andressa's files of storm track
Using wave height

TODO: Salvar a serie de indices em TXT para ler melhor aqui
"""

import pandas as pd


file = '/home/aline/Documents/Dados/tracks_andressa/TrackPar_1980_2020.txt'

# alterar este arquivo. O que esta atualmente eh o de indices 
findices = '/home/aline/Dropbox/IST_investigation/Teleconnections/AO_index.txt'

df = pd.read_csv(file,
                 sep=',',
                 index_col='Date',
                 parse_dates = True)
df = df.drop(columns='indice')

# selecionando o periodo dos indices igual ao das storms
# da Andressa
fi = pd.read_csv(findices, sep='\s+',
                names=['year', 'month', 'id'],
                header=2,
                parse_dates={'datetime':[0, 1]},
                index_col='datetime'
                )
indices_crop = fi['1980-01-01':'2019-12-31']

nstorms = df.year.resample('M').count()
nstorms_norm = (nstorms - nstorms.mean())/nstorms.std()
nstorms_norm = nstorms_norm[nstorms_norm.index.year < 2020]

nstorms_norm = nstorms_norm.reset_index(drop=True)
indices_crop = indices_crop.reset_index(drop=True)
correlation = indices_crop.corr(nstorms_norm.values, method='pearson')
plt.figure()
