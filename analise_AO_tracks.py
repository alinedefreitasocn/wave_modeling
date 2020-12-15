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
dfmensal = df.resample('M').mean()

nstorms = df.year.resample('M').count()
nstorms_norm = (nstorms - nstorms.mean())/nstorms.std()
