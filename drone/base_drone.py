import asyncio 

class BaseDrone:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def set_motors(self, motor):
        raise NotImplementedError

    @asyncio.coroutine
    def get_motion_sensors(self):
        raise NotImplementedError

    @asyncio.coroutine
    def start(self):
        raise NotImplementedError

    @asyncio.coroutine
    def stop(self):
        raise NotImplementedError

    def alive(self):
        raise NotImplementedError
