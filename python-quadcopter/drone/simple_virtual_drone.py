import asyncio
from drone import BaseVirtualDrone
import numpy as np

class SimpleVirtualDrone(BaseVirtualDrone):
    def __init__(self, motion=False):
        super().__init__()
        self.motion_on = motion
        self.motion_on = True
        
    def diff_matrix(self, omega, dt):
        olen = np.linalg.norm(omega)
        if olen:
            wx, wy, wz = omega / olen
        else:
            wx, wy, wz = 0., 0., 0.
        th = olen * dt
        K = np.array([
            [0., -wz, wy], 
            [wz, 0., -wx], 
            [-wy, wx, 0.],
        ])
        return np.eye(3) + np.sin(th) * K + (1. - np.cos(th)) * np.dot(K, K)
            # Rodrigue's formula; equivalent to exponential map exp(th*K)

    def lift(self, pomega):
        return self.LIFT_K * pomega

    def force(self, lifts): # internal frame
        f = np.array([0., 0., sum(lifts)])
        f -= self.DRAG_B * np.dot(self.rot.T, self.vel)
        return f

    def torque(self, lifts, pomega): # internal frame
        tau = np.zeros(3)
        for i in range(4):
            lf = np.array([0., 0., lifts[i]])
            tau += np.cross(self.ppos[i], lf)
            tau += np.array(
                [0., 0., .1 * (1. if i % 2 == 0 else -1.) * pomega[i]]
            )
        return tau

    def step(self, dt):
        pomega = self.motor
        rot = self.rot
        lifts = [self.lift(x) for x in pomega]
        force_int = self.force(lifts)
        torque_int = self.torque(lifts, pomega)
        force_ref = self.M * self.gvec + np.dot(rot, force_int)
        torque_ref = np.dot(rot, torque_int)
        I_ref = np.dot(np.dot(rot, self.I), self.rot.T)
        omega_ref = self.omega
        
        acc_ref = force_ref / self.M
        self.acc_sensor = np.dot(self.rot.T, acc_ref)
        rotacc_ref = np.dot(
            np.linalg.inv(I_ref),
            torque_ref - np.cross(omega_ref, np.dot(I_ref, omega_ref))
        )

        dmx = self.diff_matrix(self.omega + rotacc_ref * dt / 2., dt)
        self.rot = np.dot(dmx, self.rot)
        if self.motion_on:
            self.pos += self.vel * dt + acc_ref * dt**2 / 2.
            self.vel += acc_ref * dt
        #print(self.pos, self.vel)
        self.omega += rotacc_ref * dt

    @asyncio.coroutine
    def get_motion_sensors(self):
        acc = self.acc_sensor

        def get_real_theta():
            R = self.rot
            yaw = np.arctan2(R[1, 0], R[0, 0])
            pitch = np.arctan2(-R[2, 0], np.sqrt(R[2, 1] ** 2 + R[2, 2] ** 2))
            roll = np.arctan2(R[2, 1], R[2, 2])
            return np.array([roll, pitch, yaw])


        theta_r = get_real_theta()
        omega = np.dot(self.rot.T, self.omega) 
        z = self.pos[2] 

        return acc, theta_r, omega, z
