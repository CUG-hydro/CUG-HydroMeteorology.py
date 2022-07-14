# %%
"""
## How to use?

> ERA5数据滞后7天左右，13号，只能下载到6号的数据
> 推荐结合cdo一块使用，cdo用于nc文件的拼接

1. 登陆下面的网址，即可显示api key，形式如下：

    <https://cds.climate.copernicus.eu/api-how-to>

    ```bash
    url: https://cds.climate.copernicus.eu/api/v2
    key: 12106:faa165eb-2d80-4843-9c80-2d5e90adf***
    ```

2. 将api保存至~/.cdsapirc
"""

# %%
def make_hours():
    return ["%02d:00"%(i) for i in range(0, 24)]

def make_days(day_end):
    return ["%02d"%(i) for i in range(0, day_end+1)]

## parameters
region = [55, 75, 5, 160,] # [lat_max, lon_min, lat_min, lon_max]
year = "2022"
mons = ["07"]
days = make_days(6) # 0-31
hours = ['00:00', '06:00', '12:00', '18:00',]

prefix = "ERA5_Asia_202206-202207"

f_pres = "%s_pressure_level.nc" % prefix
f_prcp = "%s_prcp.nc" % prefix

# %%
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
        'year': year,
        'month': mons,
        'day': days,
        'time': ['00:00', '06:00', '12:00', '18:00',],
        'area': region,
        'format': 'netcdf',
    }, f_pres)

c.retrieve('reanalysis-era5-single-levels', {
        'product_type': 'reanalysis',
        'variable': 'total_precipitation',
        'year': year,
        'month': mons,
        'day': days,
        'time': make_hours(), # full hours
        'area': region,
        'format': 'netcdf',
    }, f_prcp)
#  `target=None`
# add to 
