# %%
import numpy as np
import metpy
import metpy.units

import metpy.calc as mpcalc
from metpy.calc import dewpoint, vapor_pressure

# %%

mixing_ratio = np.array([0.0004, 0.001, 0.002, 0.004, 0.007, 0.01,
                            0.016, 0.024, 0.032]).reshape(-1, 1)

# Set pressure range if necessary
# max(self.ax.get_ylim())
pressure = units.Quantity(np.linspace(600, 1000, 20), 'mbar')

# Assemble data for plotting
td = dewpoint(vapor_pressure(pressure, mixing_ratio))
td
mixing_ratio[1]
pressure[1]
vapor_pressure(pressure[1], mixing_ratio[1])

t = td[1]
t
# those two variable should be numpy array
# vapor_pressure(pressure[1], np.array([0.001]))
# vapor_pressure(c(1000, 900)*units("hPa"), np.array([0.001, 0.002]))
t, pressure
# size(t), size(pressure)
np.vstack((t.m, pressure.m)).T # [nrow, 2]

cbind(t.m, pressure.m).shape
rbind(t.m, pressure.m).shape

linedata = [np.vstack((t.m, pressure.m)).T for t in td]
# linedata
