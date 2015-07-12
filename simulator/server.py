#! /usr/bin/env python

import asyncio
import websockets
import json
import logging

from .simulator import Simulator

logger = logging.getLogger('websockets.protocol')
logger.setLevel(logging.WARNING)
logger = logging.getLogger()

class SimServer(object):
    def __init__(self, *, loop):
        self._sim = Simulator()
        self._conns = []
        self._loop = loop

    @asyncio.coroutine
    def _send(self, ws, mes):
        try:
            yield from ws.send(mes.encode())
        except websockets.exceptions.InvalidState:
            logger.warning("EInvalidState")
            return "EInvalidState"
        except Exception:
            logger.warning("G__________G")
            yield from ws.close()

    @asyncio.coroutine
    def _recv(self, ws):
        try:
            mesg = yield from ws.recv()
        except websockets.exceptions.InvalidState:
            logger.warning("EInvalidState")
            return "EInvalidState"
        except Exception as e:
            print(e)
            logger.warning("G__________G")
            yield from ws.close()
        return mesg

    @asyncio.coroutine
    def __call__(self, ws, uri):
        logger.info('concon connected')
        self._conns.append(ws)
        yield from self.run(ws)

    @asyncio.coroutine
    def run(self, ws):
        self._loop.create_task(self.send_loop(ws))
        self._loop.create_task(self.recv_loop(ws))
        while True:
            yield

    @asyncio.coroutine
    def recv_loop(self, ws):
        while ws.open:
            data = json.loads((yield from self._recv(ws)))
            if 'action' not in data:
                logger.warning('No action in data')
                return
            self._preform_action(data['action'])
            #yield from asyncio.sleep(0.02)

    def _preform_action(self, action):
        print(action)
        if action == 'start':
            self._loop.create_task(self._sim.run())

    @asyncio.coroutine
    def send_loop(self, ws):
        res = yield from self._sim.started
        if not res:
            return
        while ws.open:
            pos, ori = yield from self._sim.get_data()
            data = json.dumps({'pos':pos, 'ori':ori})
            yield from self._send(ws, data)
            yield from asyncio.sleep(0.02)

    @asyncio.coroutine
    def close(self):
        for ws in self._conns:
            yield from ws.close()
        yield from self._sim.stop()

