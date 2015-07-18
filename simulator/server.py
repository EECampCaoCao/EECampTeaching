#! /usr/bin/env python

import asyncio
import websockets
import json
import logging

logger = logging.getLogger('websockets.protocol')
logger.setLevel(logging.WARNING)
logger = logging.getLogger()

class SimulatorSocketServer(object):
    def __init__(self, sim):
        self.sim = sim
        self.conns = []
        self.loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def _send(self, ws, mes):
        try:
            yield from ws.send(mes.encode())
        except websockets.exceptions.InvalidState:
            logger.warning("EInvalidState")
            return "EInvalidState"
        except Exception as e:
            logger.error('{}'.format(e))
            yield from ws.close()

    @asyncio.coroutine
    def _recv(self, ws):
        try:
            mesg = yield from ws.recv()
            print(mesg)
        except websockets.exceptions.InvalidState:
            logger.warning("EInvalidState")
            return "EInvalidState"
        except Exception as e:
            logger.error('{}'.format(e))
            yield from ws.close()
        return mesg

    @asyncio.coroutine
    def __call__(self, ws, uri):
        logger.info('concon connected')
        self.conns.append(ws)
        yield from self.run(ws)

    @asyncio.coroutine
    def run(self, ws):
        self.loop.create_task(self.send_loop(ws))
        self.loop.create_task(self.recv_loop(ws))
        while True:
            yield

    @asyncio.coroutine
    def recv_loop(self, ws):
        while ws.open:
            data = json.loads((yield from self._recv(ws)))
            if 'action' not in data:
                logger.warning('No action in data')
                return
            yield from self._preform_action(data['action'], data['args'])
            #yield from asyncio.sleep(0.02)

    @asyncio.coroutine
    def _preform_action(self, action, args):
        if action == 'start':
            if self.sim.started.done(): return
            self.loop.create_task(self.sim.run())
        elif action == 'control':
            yield from self.sim.controller.preform_action(action, args)
        elif action == 'tweak':
            yield from self.sim.controller.preform_action(action, args)

    @asyncio.coroutine
    def send_loop(self, ws):
        res = yield from self.sim.started
        if not res:
            return
        while ws.open:
            pos, ori, motor = yield from self.sim.get_data()
            data = json.dumps({'pos':pos, 'ori':ori, 'motor': motor})
            yield from self._send(ws, data)
            yield from asyncio.sleep(0.05)

    @asyncio.coroutine
    def close(self):
        for ws in self.conns:
            yield from ws.close()
        yield from self.sim.stop()

