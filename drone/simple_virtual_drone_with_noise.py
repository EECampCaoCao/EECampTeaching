import numpy as np
from mymath.noise import apply_noise
from drone import SimpleVirtualDrone
import asyncio

class SimpleVirtualDroneWithNoise(SimpleVirtualDrone):
    def __init__(self, motion=False):
        super().__init__(motion)
        self.lift_per_motor = (np.random.normal(scale=0.05)
            + 1) * self.LIFT_K
        #self.lift_per_motor = self.LIFT_K
        self.lift_noise = 0.1
        self.acc_noise = 0.5
        self.theta_noise = 0.1
        self.omega_noise = 0.1
        self.z_noise = 1

    def lift(self, pomega):
        return self.lift_per_motor * apply_noise(
            pomega, self.lift_noise
        )

    @asyncio.coroutine
    def get_motion_sensors(self):

        acc, theta, omega, z = (yield from
            super().get_motion_sensors())

        acc = apply_noise(acc, self.acc_noise)
        theta = apply_noise(theta, self.theta_noise)
        omega = apply_noise(omega, self.omega_noise)
        z = apply_noise(z, self.z_noise)

        return acc, theta, omega, z
