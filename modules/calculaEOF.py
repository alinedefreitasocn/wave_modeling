#########################################################
# Using EOF tutorial from
# https://ajdawson.github.io/eofs/latest/examples/nao_xarray.html
#
# Begining
"""
# Create an EOF solver to do the EOF analysis.
# Square-root of cosine of
# latitude weights are applied before the computation of EOFs.
# scaling values to avoid overrepresented areas
# np.clip: Given an interval, values outside the interval are clipped to
# the interval edges. For example, if an interval of [0, 1] is specified,
# values smaller than 0 become 0, and values larger than 1 become 1.
# coslat = np.cos(np.deg2rad(m_anomalie.coords['lat'].values)).clip(0., 1.)
# coslat = np.cos(np.deg2rad(winter.coords['lat'].values)).clip(0., 1.)
"""
import numpy as np
from eofs.xarray import Eof

def calcEOF(xrdata, data_var):
    """
    input:
        xrdata: xarray Dataset
        data_var: string. Variable name to use on EOF.
    """
    coslat = np.cos(np.deg2rad(xrdata.coords['lat'].values)).clip(0., 1.)
    # np.newaxis add a dimention to wgts. dont know what ... does
    # i think its like a transposed. It took all the objects on a list and
    # make a new list with lists inside (each list with only one object)
    # just an adjustment of format
    wgts = np.sqrt(coslat)[..., np.newaxis]
    # The EOF analysis is handled by a solver class, and the EOF solution
    # is computed when the solver class is created. Method calls are then used
    # to retrieve the quantities of interest from the solver class.
    # center = False do not remove mean from data
    # solver = Eof(m_anomalie.hgt, weights=wgts, center=False)

    solver = Eof(xrdata[data_var], weights=wgts, center=False)
    # solver = Eof(s_anomalie.hgt, weights=wgts, center=False)
    # Retrieve the leading EOF, expressed as the covariance between the leading PC
    # time series and the input SLP anomalies at each grid point.
    eof1 = solver.eofsAsCovariance()
    var1 = solver.varianceFraction().sel(mode=0)

    return solver, eof1, var1
