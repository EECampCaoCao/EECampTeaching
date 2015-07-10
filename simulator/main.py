#!/usr/bin/env python

import asyncio
import websockets
import logging
import webbrowser

from .server import SimServer

from os.path import abspath, dirname, join as pjoin

async_logger = logging.getLogger("asyncio")
async_logger.setLevel(logging.WARNING)

logger = logging.getLogger()

@asyncio.coroutine
def cleanup(coros):
    logger.info('clean up...')
    for coro in coros:
        yield from coro

def run_server():
    server = SimServer()
    start_server = websockets.serve(server, 'localhost', 3000)

    loop = asyncio.get_event_loop()
    try:
        webbrowser.open(
            "file://{}".format(
                abspath(pjoin(dirname(abspath(__file__)), '..', 'WebDrone', 'index.html'))
            )
        )
        s = loop.run_until_complete(start_server)
        logger.info(
            'simulation is serving on {}'.format(s.sockets[0].getsockname())
        )
        loop.run_forever()
    except KeyboardInterrupt:
        logger.debug('capture ctrl-C in sim main.')
        coros = [
            server.close()
        ]
        loop.run_until_complete(cleanup(coros))
    finally:
        loop.close()
        logger.info("exit.")

