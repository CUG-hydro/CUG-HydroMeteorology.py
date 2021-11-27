import xarray
import xarray as xr
import numpy as np


def subset(xarr, bbox):
    """
    """
    return xarr.sel(
        lon=slice(bbox[0], bbox[1]), 
        lat=slice(bbox[3], bbox[2]))

xarray.core.dataarray.DataArray.subset = subset
xarray.core.dataset.Dataset.subset = subset


# %%
def read_grib(file, bbox = None, multi_lev=False, **kwargs):
    """
    # Parameters
    - `**kwargs`: other parameters to [xr.open_dataset()]
    """
    option_dimname = {"latitude": "lat", "longitude": "lon"}
    if multi_lev:
        option_dimname["isobaricInhPa"] = "lev"

    data = xr.open_dataset(file, backend_kwargs={"errors": "ignore"}, **kwargs)
    data = data.assign_coords(
        time=data.coords["time"].data + np.timedelta64(8, "h"))
    data = data.rename(option_dimname)
    if not(bbox is None):
        data = data.subset(bbox)
    return data


def shift_time(x, hours=6):
    """
    shift time by hours

    # Arguments:
    - `x`: xarray object
    """
    x = x.assign_coords(time=x.time.data + np.timedelta64(hours, "h"))
    return x


def ERA5_Prcp_StackOverTime(x):
    """
    - `x`: prcp 
    """
    x0 = shift_time(x.isel(step=0), hours=6)
    x1 = shift_time(x.isel(step=1), hours=12)
    x = xr.concat([x0, x1], dim="time")
    x = x.sortby("time")
    return x
