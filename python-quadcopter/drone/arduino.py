#! /usr/bin/env python3

import sys
import logging
import asyncio
import json
import random
import struct
import serial
import time
import numpy as np

logger = logging.getLogger()

class Arduino(object):
    def __init__(self, *, loop=None):
        if loop:
            self._loop = loop
        else:
            self._loop = asyncio.get_event_loop()

        self._waitings = asyncio.Queue(loop=self._loop)
        self.state = 'INIT'
    
    def _get_data(self):
        try:
            fut, s = self._waitings.get_nowait()
            while fut.done():
                fut, s = self._waitings.get_nowait()
            res = self._ser.read(s)
            fut.set_result(res)
        except asyncio.QueueEmpty:
            res = self._ser.read(self._ser.inWaiting())
            logger.error('arduino yapsilon!!!! {}'.format(res))
        except KeyboardInterrupt:
            logger.warning('reading from arduino was cancelled by Ctrl-C.')
            fut.set_result(False)

    @asyncio.coroutine
    def communicate(self, cmd, size=None):
        try:
            if not size:
                self._ser.write(cmd)
                self._ser.flush()
                return

            w = asyncio.Future(loop=self._loop)
            self._waitings.put_nowait((w, size))
            retry = 0
            res = None
            while not w.done() and retry <= 10:
                self._ser.write(cmd)
                self._ser.flush()
                try:
                    res = yield from asyncio.wait_for(asyncio.shield(w), 3.5)
                except asyncio.TimeoutError:
                    retry += 1
                    logger.debug('Retry {}'.format(retry))
                else:
                    break
        except serial.serialutil.SerialException:
            logger.warning('arduino was not connected.')
            return

        if res is None:
            self.state = 'FAILED'
            logger.critical('飛機con掉了...好慘喔...QQQ')
            w.cancel()

        return res

    @asyncio.coroutine
    def setup(self):
        '''
        initialize the connection with arduino using serial
        '''
        try:
            self._ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=3)
        except serial.serialutil.SerialException:
            logger.error('Arduino was not connected to Rpi !!')
            self.state = 'FAILED'
            return

        self._loop.add_reader(self._ser.fileno(), self._get_data)
        logger.info('start setup...')
        while True:
            ret = yield from self.communicate(b'S', 1)
            if ret == b's':
                logger.info('Connected with Arduino.')
                self.state = 'CONNECTED'
                break
            elif ret == b'':
                logger.info('Waiting for Arduino...')
            else:
                logger.error('Communication with Arduino failed !!'
                             ' (received {})'.format(ret))
                self.state = 'FAILED'

    def verify_sensors(self, data):
        acc = data['accel']
        omega = data['gyro']
        mag = data['mag']
        temp = data['temperature']
        p = data['pressure']
        if (np.linalg.norm(acc) > 100 or np.linalg.norm(omega) > 100 
                or np.linalg.norm(mag) > 1.1 
                or np.linalg.norm(mag) < 0.9 or temp < 0 or temp > 45
                or p < 90000 or p > 110000):
            return False
        return True

    def convert_sensors(self, data):
        data['accel'] = list(map(lambda x: x * 2 * 9.8 / 32768. , data['accel']))
        data['gyro'] = list(map(lambda x: x * np.pi / 180 * 250 / 32768. ,
                                data['gyro']))
        mag_norm = np.linalg.norm(data['mag'])
        data['mag'] = list(map(lambda x: x / mag_norm , data['mag']))
        volrate = 0.9755
        data['voltage'] *= volrate * 10.16
        data['current'] = volrate * data['current'] * 16.6 + 0.73
        return data

    def decode_sensors(self, b):
        '''
        decode sensors data from bytes to dict.
        '''
        
        if not b:
            return None

        res = []
        retsize = [
            ('accel', 'h', 3),
            ('gyro', 'h', 3),
            ('mag', 'h', 3),
            ('temperature', 'f', 1),
            ('pressure', 'f', 1),
            ('voltage', 'f', 1),
            ('current', 'f', 1),
        ]
        ret = {}
        ret['time'] = self._loop.time()
        scnt = 0
        for t, c, s in retsize:
            if c == 'h':
                byte = s * 2
            elif c == 'f':
                byte = s * 4
            ret[t] = list(struct.unpack(c*s, b[scnt:(scnt+byte)]))
            if len(ret[t]) == 1:
                ret[t] = ret[t][0]
            scnt += byte

        ret = self.convert_sensors(ret)

        if not self.verify_sensors(ret):
            return None


        return ret

    def unpack_data(self, b, retsize):
        ret = {}
        ret['time'] = self._loop.time()
        scnt = 0
        for t, c, s in retsize:
            if c == 'h':
                byte = s * 2
            elif c == 'f':
                byte = s * 4
            ret[t] = list(struct.unpack(c*s, b[scnt:(scnt+byte)]))
            if len(ret[t]) == 1:
                ret[t] = ret[t][0]
            scnt += byte
        return ret
        

    @asyncio.coroutine
    def read_motion_sensors(self):
        '''
        read sensors from arduino.
        '''
        # ax, ay, az, gx, gy, gz, mx, my, mz
        #  2,  2,  2,  2,  2,  2,  2,  2,  2 = 18
        data = None
        while data is None:
            data = yield from self.communicate(b'R', 2*9)

        retsize = [
            ('accel', 'h', 3),
            ('gyro', 'h', 3),
            ('mag', 'h', 3),
        ]
        data = self.unpack_data(data, retsize)
        data['accel'] = list(map(lambda x: x * 2 * 9.8 / 32768. , data['accel']))
        data['gyro'] = list(map(lambda x: x * np.pi / 180 * 250 / 32768. ,
                                data['gyro']))
        mag_norm = np.linalg.norm(data['mag'])
        data['mag'] = list(map(lambda x: x / mag_norm , data['mag']))

        if (np.linalg.norm(data['accel']) > 100 
                or np.linalg.norm(data['gyro']) > 100 
                or np.linalg.norm(data['mag']) > 1.1 
                or np.linalg.norm(data['mag']) < 0.9):
            return None
        return data

    @asyncio.coroutine
    def read_weather_sensors(self):
        '''
        temp, pres
           4,    4 = 
        '''
        data = None
        while data is None:
            data = yield from self.communicate(b'W', 4*2)
        retsize = [
            ('temperature', 'f', 1),
            ('pressure', 'f', 1),
        ]
        data = self.unpack_data(data, retsize)
        if (data['temperature'] < 0 or data['temperature'] > 45
            or data['pressure'] < 90000 or data['pressure'] > 110000):
            return None
        return data

    @asyncio.coroutine
    def read_voltage_sensors(self):
        '''
        temp, pres, voltage, current
           4,    4,       4,       4 = 34        data = None
        '''
        data = None
        while data is None:
            data = yield from self.communicate(b'V', 4*2)
        retsize = [
            ('voltage', 'f', 1),
            ('current', 'f', 1),
        ]
        data = self.unpack_data(data, retsize)
        volrate = 0.9755
        data['voltage'] *= volrate * 10.16
        data['current'] = volrate * data['current'] * 16.6 + 0.73
        return data

    @asyncio.coroutine
    def write_motors(self, motors):
        '''
        send control signals to drone's motors via arduino.
        motors - a list containing four int numbers which indicate
                 the control signals for drone's motors.
        '''
        yield from self.communicate(b'M')
        st = struct.pack('hhhh', *motors)
        res = yield from self.communicate(st, 1)
        if res != b'm':
            logger.error('Write motor to Arduino failed !!!')

    def alive(self):
        return self.state != 'FAILED' and self.state != 'CLOSED'

    def close(self):
        self._loop.run_until_complete(
            self.write_motors([-20, -20, -20, -20])
        )
        if self.state != 'CLOSED':
            self._ser.flush()
            self._ser.close()
            self.state = 'CLOSED'


# use in arduino mode
def run_arduino():
    loop = asyncio.get_event_loop()
    arduino = Arduino()

    @asyncio.coroutine
    def read_stdin():
        yield from arduino.setup()
        reader = asyncio.StreamReader()
        reader_protocol = asyncio.StreamReaderProtocol(reader)
        yield from loop.connect_read_pipe(lambda: reader_protocol, sys.stdin)
        while True:
            data = (yield from reader.readline()).decode().strip()
            if data == 'R' or data=='W' or data=='V':
                res = []
                TN = 100
                for i in range(TN):
                    if data == 'R':
                        s = yield from arduino.read_motion_sensors()
                    elif data == 'W':
                        s = yield from arduino.read_weather_sensors()
                    else: 
                        s = yield from arduino.read_voltage_sensors()
                    res.append(s)
                s = {}
                for k in res[0]:
                    s[k] = sum(np.array(res[i][k]) for i in range(TN)) / TN
                logger.debug(s)
                continue
            try:
                motors = [int(x) for x in data.split()]
                if len(motors) != 4:
                    continue
                yield from arduino.write_motors(motors)
            except IOError as e:
                logger.error(e)
            except ValueError:
                pass
    
    try:
        loop.run_until_complete(read_stdin())
    except KeyboardInterrupt:
        print("stoping..., please press Ctrl-C again")
    finally:
        print('exit.')

if __name__ == "__main__":
    run_arduino()
