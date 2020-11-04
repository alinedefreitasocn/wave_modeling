import cdstoolbox as ct


@ct.application(title='Compute Climatology')
@ct.input.dropdown('variable', values=['2m_temperature', 'mean_sea_level_pressure'])
@ct.input.dropdown('frequency', default='month', values=['dayofyear', 'weekofyear', 'month'])
@ct.output.livefigure()
def compute_climatology(variable, frequency):
    """
    Compute climatology mean and standard deviation for a specific location.
    Plot results on a line plot.
    """

    data = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels',
        {
            'variable': variable,
            'grid': ['3', '3'],
            'product_type': 'reanalysis',
            'year': [
                '2008','2009','2010',
                '2011','2012','2013',
                '2014','2015','2016',
                '2017'
            ],
            'month': [
                '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12'
            ],
            'day': [
                '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12',
                '13', '14', '15', '16', '17', '18',
                '19', '20', '21', '22', '23', '24',
                '25', '26', '27', '28', '29', '30',
                '31'
            ],
            'time': ['00:00', '06:00', '12:00', '18:00'],
        }
    )

    data_location = ct.geo.extract_point(data, lon=-1, lat=51.5)
    clima_mean = ct.climate.climatology_mean(data_location, frequency=frequency)
    clima_std = ct.climate.climatology_std(data_location, frequency=frequency)
    fig = ct.chart.plot_climatology(clima_mean, error_y=clima_std)

    return fig
