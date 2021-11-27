from scipy.ndimage import gaussian_filter
from metpy.units import units


def smooth_uv(u, v, sigma=3.0, unit = units('m/s')):
    """
    # Arguments:
    - `unit`: `units('m/s')`
    """
    u = gaussian_filter(u.data, sigma=sigma) * unit
    v = gaussian_filter(v.data, sigma=sigma) * unit
    return u, v
