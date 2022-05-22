import numpy as np
import os
from glob import glob 


def as_rowvec(x):
    return np.reshape(x, (1, -1))


def as_colvec(x):
    return np.reshape(x, (-1, 1))


# the default is `colvec`
as_matrix = as_colvec

def rbind(x, y):
    if x is None: return y
    if y is None: return x

    if len(x.shape) == 1:
        x = as_rowvec(x)
    if len(y.shape) == 1:
        y = as_rowvec(y)
    return np.concatenate((x, y), axis=0)


def cbind(x, y):
    if x is None: return y
    if y is None: return x
    
    if len(x.shape) == 1:
        x = as_colvec(x)
    if len(y.shape) == 1:
        y = as_colvec(y)
    return np.concatenate((x, y), axis=1)


# np.linspace(0, 1, )
# c = lambda *args, **keywords: np.array(*args, **keywords)
def c(*args, **kwargs):
    return np.array([*args], **kwargs)

def seq(start, stop = None, by = 1, len = None):
    """
    seq(start, stop = None, by = 1, len = None)
    
    # Examples
    ```python
    seq(3) = c(1, 2, 3)
    seq(3, 6) = c(3, 4, 5)# not include the last
    seq(3, 6, 2) = c(3, 6)
    ```
    """
    if len != None:
        return np.linspace(start, stop, len)
    else:
        if stop != None: stop += by
        return np.arange(start, stop, by)
    # seq = lambda *args, **keywords: np.arange(*args, **keywords)


def r_dir(path, pattern = "*"):
  path = os.path.join(path, pattern)
  return glob(path)
