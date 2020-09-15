#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 17:57:41 2020

@author: aline
"""

import cdsapi

c = cdsapi.Client()

years = ['1989', '1990', '1991', '1992',
            '1993', '1994', '1995',
            '1996', '1997', '1998',
            '1999', '2000', '2001',
            '2002', '2003', '2004',
            '2005', '2006', '2007',
            '2008', '2009', '2010',
            '2011', '2012', '2013',
            '2014', '2015', '2016',
            '2017', '2018', '2019'
            ]
months = [
	    '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
	]
data = ['hourly', 'monthly_mean']

if data = 'hourly':
    for y in years:
        for m in months:
            c.retrieve(
                'reanalysis-era5-single-levels',
                {
                    'product_type': 'reanalysis',
                    'format': 'grib',
                    'variable': [
                        '10m_u_component_of_wind',
                        '10m_v_component_of_wind',
                        'mean_wave_direction',
                        'mean_wave_period',
                        'significant_height_of_combined_wind_waves_and_swell',
                    ],
                    'year': [ y,

                    ],
                    'month': [ m,

                    ],
                    'day': [
                        '01', '02', '03',
                                '04', '05', '06',
                                '07', '08', '09',
                                '10', '11', '12',
                                '13', '14', '15',
                                '16', '17', '18',
                                '19', '20', '21',
                                '22', '23', '24',
                                '25', '26', '27',
                                '28', '29', '30',
                                '31',
                    ],
                    'time': [
                        '00:00', '01:00', '02:00',
                                '03:00', '04:00', '05:00',
                                '06:00', '07:00', '08:00',
                                '09:00', '10:00', '11:00',
                                '12:00', '13:00', '14:00',
                                '15:00', '16:00', '17:00',
                                '18:00', '19:00', '20:00',
                                '21:00', '22:00', '23:00',
                    ],
                    'area': [
                            90, -180, 0,
                            180,
                    ],
                },
                '/home/aline/Documents/ERA5/' + y + m + '.grib')



# For montly mean data
elif data = 'monthly_mean':
    for y in years:
        for m in months:
            c.retrieve(
                'reanalysis-era5-single-levels-monthly-means',
                {
                    'format': 'netcdf',
                    'product_type': [
                        'monthly_averaged_reanalysis',
                    ],
                    'variable': [
                        '10m_wind_speed', 'instantaneous_10m_wind_gust', 'mean_wave_direction',
                        'mean_wave_period', 'significant_height_of_combined_wind_waves_and_swell',
                    ],
                    'year': [y,
                    ],
                    'month': [m,
                    ],
                    'time': '00:00',
                    'area': [
                            90, -100, 0,
                            20,
                    ],
                },
                '/home/aline/Documents/ERA5/montly_mean' + y + '_'+ m + '.nc')


# For montly mean data
elif data = 'monthly_mean':
    for y in years:
        for m in months:
            c.retrieve(
                'reanalysis-era5-single-levels-monthly-means',
                {
                    'format': 'grib',
                    'product_type': [
                        'monthly_averaged_reanalysis',
                    ],
                    'variable': [
                        # '10m_wind_speed', 'instantaneous_10m_wind_gust',
                        'mean_wave_direction',
                        'mean_wave_period', 'significant_height_of_combined_wind_waves_and_swell',
                    ],
                    'year': ['1989', '1990', '1991', '1992',
                                '1993', '1994', '1995',
                                '1996', '1997', '1998',
                                '1999', '2000', '2001',
                                '2002', '2003', '2004',
                                '2005', '2006', '2007',
                                '2008', '2009', '2010',
                                '2011', '2012', '2013',
                                '2014', '2015', '2016',
                                '2017', '2018', '2019',
                    ],
                    'month': ['01', '02', '03',
                        '04', '05', '06',
                        '07', '08', '09',
                        '10', '11', '12',
                    ],
                    'time': '00:00',
                    'area': [
                            90, -100, 0,
                            20,
                    ],
                },
                '/home/aline/Documents/ERA5/montly_mean_1990_2020.grib')
