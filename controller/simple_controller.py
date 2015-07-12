#! /usr/bin/env python3

import asyncio
import logging
import json
import numpy as np

from mymath import PID, Momentum, ThetaOmegaKalmanFilter
from .constant import CONST

from controller import BaseController

logger = logging.getLogger()

class SimpleController(BaseController):
    def __init__(self, drone, *, loop=None, log=False):

        super().__init__(drone)

        self.kf = []
        for i in range(3):
            self.kf.append(ThetaOmegaKalmanFilter(0.1, 0.1, 0.04))
        self.action = np.array([0., 0., 0., 0.])
        self.thrust = 0

        self.accz_momentum = Momentum(tau=0.05)

        self.target_theta = np.array([0., 0., 0.])
        self.target_omegaz = 0.
        self.target_zacc = 9.8

        self.pid_thetaxy = np.array([48., 40., 15.])
        self.pid_tweakper = np.array([1., 1., 1.])

        self.pids = {
            'theta_x': PID(*self.pid_thetaxy, imax=60.),
            'theta_y': PID(*self.pid_thetaxy, imax=60.),
            'theta_z': PID(60., 20., 30., imax=60.),
            'acc_z': PID(20., 1., 0., imax=800),
        }

    @asyncio.coroutine
    def update(self):
        '''updates the motors according to the sensors' data
        '''
        now = self.loop.time()
        dt = now - self.last_time

        self.target_theta[2] += dt * self.target_omegaz

        acc, theta, omega, z = yield from self.drone.get_motion_sensors()

        theta_smooth = []
        omega_smooth = []
        for i in range(3):
            theome = np.array([theta[i], omega[i]])
            self.kf[i].update(now, theome)
            the, ome = self.kf[i].predict(now)
            theta_smooth.append(the)
            omega_smooth.append(ome)
        theta_smooth = np.array(theta_smooth)
        omega_smooth = np.array(omega_smooth)

        zacc_smooth = self.accz_momentum.append_value(now, acc[2])

        theta_error = self.target_theta - theta_smooth
        zacc_error  = self.target_zacc  - zacc_smooth

        theta_x_action = self.pids['theta_x'].get_control(
            now, theta_error[0], 0 - omega_smooth[0]
        )
        theta_y_action = self.pids['theta_y'].get_control(
            now, theta_error[1], 0 - omega_smooth[1]
        )
        theta_z_action = self.pids['theta_z'].get_control(
            now, theta_error[2], 0 - omega_smooth[2]
        )

        thrust_action = self.pids['acc_z'].get_control(
            now, 0 - zacc_smooth
        )

        action = np.array([-theta_y_action +  theta_z_action,
                            theta_x_action + -theta_z_action,
                            theta_y_action +  theta_z_action,
                           -theta_x_action + -theta_z_action,])
        action += thrust_action

        yield from self.send_control(action)

        self.last_time = now

        # logging
        if self.logger:
            self.logger.info(json.dumps({
                'action': self.action.tolist(),
                'accel': acc.tolist(),
                'theta': theta.tolist(),
                'omega': omega.tolist(),
                'theta_smooth': theta_smooth.tolist(),
                'omega_smooth': omega_smooth.tolist(),
                'time': now,
            }))

    @asyncio.coroutine
    def send_control(self, action=None, thrust=None):
        if action is not None: self.action = action
        if thrust is not None: self.thrust = thrust

        final_action = self.action + self.thrust
        final_action = np.maximum.reduce([final_action,
                                          np.full((4,), -100)])
        final_action = np.minimum.reduce(
            [final_action, np.full((4,), CONST['thrust_restriction'])]
        )
        yield from self.drone.set_motors(final_action)


    @asyncio.coroutine
    def preform_action(self, action, args):
        if action == 'stop':
            yield from self.stop()
        elif action == 'arm':
            print('Get Arm')
            yield from self.arm()
        elif action == 'disarm':
            yield from self.disarm()
        elif action == 'control':
            self.preform_control(*args)
        elif action == 'tweak':
            self.tweak_pid(*args)
    
    def preform_control(self, thrust, theta_x, theta_y, omega_z):
        self.target_zacc = 9.8 + thrust
        self.target_theta[0] = theta_x
        self.target_theta[1] = theta_y
        self.target_omegaz = omega_z

    def tweak_pid(self, type_, per):
        if type_ == 'P':
            self.pid_tweakper[0] = per
        elif type_ == 'I':
            self.pid_tweakper[1] = per
        elif type_ == 'D':
            self.pid_tweakper[2] = per
        gain = self.pid_thetaxy * self.pid_tweakper
        for x in self.pids.values():
            x.set_gain(*gain)
            


