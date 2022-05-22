import pandas as pd



def xr_date(ds):
  return pd.to_datetime(ds["time"].values)

def date(x):
  # convert datetime64 to date
  return pd.to_datetime(x).date

def hour(x):
  return pd.to_datetime(x).hour.tolist()
