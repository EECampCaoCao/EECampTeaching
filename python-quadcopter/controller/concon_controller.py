#! /usr/bin/env python3

import asyncio
import logging
import json
import numpy as np

from mymath import (MyPID as PID, Momentum, ThetaOmegaKalmanFilter,
    PositionAccelerationKalmanFilter)
from .constant import CONST

from controller import SimpleController

logger = logging.getLogger()

class ConConController(SimpleController):
    @asyncio.coroutine
    def send_control(self, action=None, thrust=None):
        if action is not None: self.action = action
        if thrust is not None: self.thrust = thrust

        final_action = np.full(4., 20.)
        yield from self.drone.set_motors(final_action)



