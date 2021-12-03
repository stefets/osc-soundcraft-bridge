#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import signal
import socket
import colorama

from osc_server import OscServer
from soundcraft_client import SoundCraftClient


# Config file
sys.path.append(os.path.realpath('.'))
with open('config.json') as json_file:
    configuration = json.load(json_file)


osc = None
client = None

def start_osc():
    global client
    global osc
    osc = OscServer(configuration["osc"]["listen_port"], client)
    osc.run_forever()
    print('OSC server running.')


def connect_mixer():
    global client
    config = configuration["soundcraft"]
    client = SoundCraftClient(config["version"], config["ip"], config["port"])
    client.run_forever()


def signal_handler(signum, frame):
    print(f"Signal {signum} received.")
    dispose()


def dispose():
    global client
    if client:
        client.exit_event.set()
        client.terminate()

    global osc
    if osc:
        osc.terminate()
        print("OSC server stopped gracefully.")


def main(args=None):
    signal.signal(signal.SIGINT, signal_handler)
    try:
        connect_mixer()
        start_osc()
        signal.pause()
    except (socket.timeout):
        print("SoundCratf disconnected.")
        dispose()
    finally:
        print("All services disposed.")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
