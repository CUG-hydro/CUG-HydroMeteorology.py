import xarray
import xarray as xr
import numpy as np


def get_coords(ds):
    dimnames = list(ds.coords)
    dim_lon = [i for i in dimnames if "lon" in i][0]
    dim_lat = [i for i in dimnames if "lat" in i][0]
    lon = ds[dim_lon].values
    lat = ds[dim_lat].values
    return lon, lat


def subset(xarr, bbox):
    """
    """
    return xarr.sel(
        lon=slice(bbox[0], bbox[1]), 
        lat=slice(bbox[3], bbox[2]))

xarray.core.dataarray.DataArray.subset = subset
xarray.core.dataset.Dataset.subset = subset


# %%
def read_grib(file, bbox = None, timezone = 8, multi_lev=False, **kwargs):
    """
    # Parameters
    - `**kwargs`: other parameters to [xr.open_dataset()]
    """
    option_dimname = {"latitude": "lat", "longitude": "lon"}
    if multi_lev:
        option_dimname["isobaricInhPa"] = "lev"

    ds = xr.open_dataset(file, backend_kwargs={"errors": "ignore"}, **kwargs)
    ds = set_timezone(ds, timezone = timezone)
    data = data.rename(option_dimname)
    if not(bbox is None):
        data = data.subset(bbox)
    return data

def shift_time(time, hours=6):
    """
    shift time by hours
    #!DEPRECATED

    # Arguments:
    - `x`: xarray object
    """
    x = x.assign_coords(time=x.time.data + np.timedelta64(hours, "h"))
    return x
    
def set_timezone(ds, timezone = 8):
    time = ds.coords["time"].data + np.timedelta64(timezone, "h")
    return ds.assign_coords(time = time)

def read_nc(file, bbox = None, timezone = 8, **kwargs):
    ds = xr.open_dataset(file, **kwargs)
    ds = set_timezone(ds, timezone = timezone)
    if not(bbox is None):
        data = data.subset(bbox)
    return data


def ERA5_Prcp_StackOverTime(x):
    """
    - `x`: prcp 
    """
    x0 = shift_time(x.isel(step=0), hours=6)
    x1 = shift_time(x.isel(step=1), hours=12)
    x = xr.concat([x0, x1], dim="time")
    x = x.sortby("time")
    return x
