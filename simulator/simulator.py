#! /usr/bin/env python3

import asyncio
import logging
# import matplotlib.pyplot as plt
import numpy as np

from drone import (SimpleVirtualDrone,
        SimpleVirtualDroneWithNoise)

from controller import SimpleController

logger = logging.getLogger()

np.set_printoptions(precision=10, suppress=True)

class Simulator(object):
    def __init__(self):
        self._drone = SimpleVirtualDroneWithNoise()
        #self._drone = SimpleVirtualDrone()
        self._controller = SimpleController(self._drone, log=True)
        self._loop = asyncio.get_event_loop()
        #self._drone.set_init([0., 0., 0.], [0., 0., 1.])
        self.started = asyncio.Future()
        # self._AOO = []
        # self._drone.dt = 5e-4
        # self._drone.noise_z = 1e-10

    @asyncio.coroutine
    def run(self):
        logger.info('starting simulation...')
        yield from self._controller.arm()
        self._loop.call_soon_threadsafe(
            self._loop.create_task,
            self._controller.start()
        )
        self.started.set_result(True)
        logger.info('started.')

    @asyncio.coroutine
    def get_data(self):
        pos = list(self._drone.pos)
        ori = list(self._drone.rot.flatten())
        motor = list(self._drone.motor.flatten())
        # oori = ori[:, 2]
        # self._AOO.append(self._drone.acc_sensor[2])
        # self._AOO.append(oori)
        return pos, ori, motor

    @asyncio.coroutine
    def stop(self):
        yield from self._controller.stop()
        yield from self._drone.stop()
        # logger.debug('plotting...')
        # plt.plot(self._AOO)
        # plt.show()
