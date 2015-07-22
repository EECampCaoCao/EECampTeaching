import asyncio
import logging
import json
import numpy as np

from controller.constant import CONST

logger = logging.getLogger()

class BaseController(object):
    def __init__(self, drone, *, log=False):

        self.loop = asyncio.get_event_loop()
        self.armed = False
        self.drone = drone
        self.action = np.array([0., 0., 0., 0.])

        self.stopped = False

        # logging
        self.logger = None
        if log:
            self.logger_setup()

    def logger_setup(self):
        self.logger = logging.getLogger('data')
        self.logger.propagate = False
        fh = logging.FileHandler('action.log')
        self.logger.addHandler(fh)

    @asyncio.coroutine
    def start(self):
        try:
            yield from self.drone.start()
            logger.info('controller started.')
            self.loop.create_task(self.run())
        except KeyboardInterrupt:
            logger.info('capture ctrl-C in controller.')

        return True

    @asyncio.coroutine
    def run(self):
        self.last_time = self.loop.time()

        while self.drone.alive() and not self.stopped:
            if self.armed:
                yield from self.update()
            yield from asyncio.sleep(.0)


    @asyncio.coroutine
    def update(self):
        raise NotImplementedError

    @asyncio.coroutine
    def arm(self):
        self.armed = True
        yield from self.send_control(thrust=CONST['armed_thrust'])
    
    @asyncio.coroutine
    def disarm(self):
        self.armed = False
        yield from self.send_control(thrust=CONST['disarmed_thrust'])

    @asyncio.coroutine
    def stall(self):
        yield from self.send_control(thrust=CONST['disarmed_thrust'])

    @asyncio.coroutine
    def stop(self):
        self.stopped = True
        yield from self.stall()

    @asyncio.coroutine
    def preform_action(self, action, args):
        raise NotImplementedError
            


