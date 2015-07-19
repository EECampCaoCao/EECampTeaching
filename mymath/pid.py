#! /usr/bin/env python3

import numpy as np

class BasePID:
    def __init__(self, kp, ki, kd, *, imax):
        self.imax = imax
        self.set_gain(kp, ki, kd)

    def set_gain(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.int_restriction = self.imax / (self.ki + 1e-10)


class PID(BasePID):
    def __init__(self, kp, ki, kd, *, imax):
        super().__init__(kp, ki, kd, imax=imax)
        self.last_time = None
        self.last_err = None
        self.int_err = 0

    def get_control(self, t, err, derr=None):
        up = err * self.kp 
        if self.last_err is None:
            self.last_err = err

        if self.last_time is None:
            self.last_time = t
            return up

        dt = t - self.last_time + 1e-10
        if derr is None:
            derr = (err - self.last_err) / dt

        ud = derr * self.kd

        self.int_err += err * dt

        if self.int_err > self.int_restriction:
            self.int_err = self.int_restriction

        if self.int_err < -self.int_restriction:
            self.int_err = -self.int_restriction

        ui = self.int_err * self.ki

        self.last_err = err
        self.last_time = t

        return (up + ud + ui)


