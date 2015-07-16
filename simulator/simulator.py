#! /usr/bin/env python3

import asyncio
import logging
# import matplotlib.pyplot as plt
import numpy as np

from drone import (SimpleVirtualDrone,
        SimpleVirtualDroneWithNoise)

from controller import SimpleController
from simulator.HTTPserver import start_HTTPserver
from simulator.server import SimulatorSocketServer

import websockets
import webbrowser

logger = logging.getLogger()

np.set_printoptions(precision=10, suppress=True)

class Simulator(object):
    def __init__(self):
        self._drone = SimpleVirtualDroneWithNoise()
        #self._drone = SimpleVirtualDrone()
        self._controller = SimpleController(self._drone, log=True)
        self.loop = asyncio.get_event_loop()
        #self._drone.set_init([0., 0., 0.], [0., 0., 1.])
        self.started = asyncio.Future()
        # self._AOO = []
        # self._drone.dt = 5e-4
        # self._drone.noise_z = 1e-10

    def start(self):
        s = self.start_server()
        logger.info(
            'simulation is serving on {}'.format(s.sockets[0].getsockname())
        )
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            logger.debug('capture ctrl-C in sim main.')
            self.loop.run_until_complete(self.stop())
        finally:
            self.loop.close()
            logger.info("exit.")

    @asyncio.coroutine
    def run(self):
        logger.info('starting simulation...')
        yield from self._controller.arm()
        self.loop.call_soon_threadsafe(
            self.loop.create_task,
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

    def start_server(self):
        socket_server = SimulatorSocketServer(self)
        start_socket_server = websockets.serve(socket_server,
            'localhost', 3000)
        start_HTTPserver()

        @asyncio.coroutine
        def open_browser():
            yield from asyncio.sleep(1.)
            webbrowser.open(
                "http://localhost:8000/WebDrone/index.html"
            )

        self.loop.create_task(open_browser())
        return self.loop.run_until_complete(start_socket_server)

