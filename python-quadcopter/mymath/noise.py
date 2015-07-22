import numpy as np

def apply_noise(x, sc):
    if sc == 0:
        return x
    elif type(x) is np.ndarray:
        return x + np.random.normal(scale=sc, size=x.shape)

    return x + np.random.normal(scale=sc)


