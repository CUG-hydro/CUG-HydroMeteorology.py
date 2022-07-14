# %%
import numpy as np
import xarray as xr
import pandas as pd
import datetime

import os
from os import mkdir
from pathlib import Path


_init=False

def set_cwd():
  global _init
  if not _init:
    _init=True
    workdir = str(Path('.').absolute().parent)
    print("running here!")
    os.chdir(workdir)
    print("Current working dir: ", os.getcwd())

## 把路径添加进来
# import sys
# pkg_dir = workdir + "/rbase"
# sys.path.append(workdir)

workdir = "D:\GitHub\cug-hydro\CUG-HydroMeteorology.py"
os.chdir(workdir)

print("working dir: ", os.getcwd())

# set_cwd()
from rbase import *
