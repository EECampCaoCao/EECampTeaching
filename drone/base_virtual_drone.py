import asyncio
from drone import BaseDrone
import numpy as np
import logging

logger = logging.getLogger()

class BaseVirtualDrone(BaseDrone):
    def __init__(self):
        super().__init__()
        # Some Constant
        self.g = 9.80
        self.gvec = np.array([0., 0., -self.g])
        self.M = 1.250
        self.R = 0.23
        self.Iz = 0.25 * self.M * self.R**2
        self.Ixy = self.Iz * 0.5
        self.I = np.diag([self.Ixy, self.Ixy, self.Iz])
        self.LIFT_K = 7.5e-3
        self.DRAG_B = 0.5
        self.ppos = [
            np.array([self.R, 0., 0.]),
            np.array([0., self.R, 0.]),
            np.array([-self.R, 0., 0.]),
            np.array([0., -self.R, 0.]),
        ]
        self.pdir = [1., -1., 1., -1.]

        # Some physic quantity
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.rot = np.eye(3)
        self.omega = np.zeros(3)
        self.acc_sensor = np.array([0, 0, self.g])
        self.motor = np.zeros(4)

        q = 0.8
        self.rot = np.array([[1, 0, 0],
                             [0, np.cos(q), -np.sin(q)],
                             [0, np.sin(q), np.cos(q)]])

    def step(self, dt):
        raise NotImplementedError

    def get_time(self):
        return self.loop.time()

    @asyncio.coroutine
    def run(self):
        last_time = self.get_time()
        while True:
            try:
                yield from asyncio.sleep(0.0002)
                now = self.get_time()
                dt = now - last_time
                self.step(dt)
                last_time = self.get_time()
            except asyncio.CancelledError:
                logger.debug('stop simulation.')
                break
            except KeyboardInterrupt:
                logger.debug('capture ctrl-C in virtual drone._run().')
                break

    @asyncio.coroutine
    def start(self):
        self._worker = self.loop.create_task(self.run())

    def alive(self):
        return not self._worker.done()

    @asyncio.coroutine
    def set_motors(self, motor):
        self.motor = np.maximum(np.minimum(motor, 700), 0)
        asyncio.sleep(0.01)

