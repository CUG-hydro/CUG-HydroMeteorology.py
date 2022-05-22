import numpy as np
import xarray as xr
import pandas as pd
import datetime

import os
# import sys
from pathlib import Path

workdir = str(Path('.').absolute().parent)
os.chdir(workdir)
# sys.path.append()
from rbase import *
