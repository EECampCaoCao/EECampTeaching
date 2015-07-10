import asyncio
import logging
import numpy as np
import scipy.linalg

logger = logging.getLogger()

class Drone(object):
    def __init__(self):
        self.g = 9.80
        self.gvec = np.array([0., 0., -self.g])
        self.M = 1.250
        self.R = 0.23
        self.Iz = 0.1 * self.M * self.R**2
        self.Ixy = self.Iz * 0.5
        self.I = np.diag([self.Ixy, self.Ixy, self.Iz])
        self.LIFT_K = 7.5e-3
        self.TDRAG_K = 0.0
        self.DRAG_B = 0.5


