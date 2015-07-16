#! /usr/bin/env python3

import logging
import argparse

#from simulator import run_server as sim_server

from logsetting import log_setup
from importlib import import_module

from os import listdir
from os.path import curdir, abspath, join as pjoin

scripts = list(map(lambda x: x[:-3], 
               filter(lambda x: x[-3:] == '.py',
    listdir(pjoin(abspath(curdir), 'scripts')))))

parser = argparse.ArgumentParser(description='Drone control and simulation.')
parser.add_argument('-s', '--script', help='which script to execute', type=str,
                    choices=scripts, required=True)
parser.add_argument('-f', '--logfile', help='log file', default=None)
parser.add_argument('-l', '--loglevel', help='log level',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    default='DEBUG')

if __name__ == '__main__':
    args = parser.parse_args()
    log_setup(level=args.loglevel, filepath=args.logfile)
    Main = import_module('scripts.{}'.format(args.script))
    Main.main()
