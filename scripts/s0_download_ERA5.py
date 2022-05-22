import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            'geopotential', 'specific_humidity', 'u_component_of_wind',
            'v_component_of_wind',
        ],
        'pressure_level': ['200', '500', '850',],
        'year': '2022',
        'month': '05',
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17',
        ],
        'time': ['00:00', '06:00', '12:00', '18:00',],
        'area': [55, 75, 5, 160,],
        'format': 'netcdf',
    },
    'ERA5_202205_Asia.nc')

c.retrieve('reanalysis-era5-single-levels', {
        'product_type': 'reanalysis',
        'variable': 'total_precipitation',
        'year': '2022',
        'month': '05',
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
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
        'area': [55, 75, 5, 160],
        'format': 'netcdf',
    },
    'ERA5_202205_Asia_prcp.nc')
