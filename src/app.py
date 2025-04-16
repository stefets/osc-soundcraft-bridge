#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import json
import signal
import socket
import threading

from services.soundcraft import Mixer
from services.py_osc import OscServer


# Config file
sys.path.append(os.path.realpath('.'))
with open('config.json') as json_file:
    configuration = json.load(json_file)
    

osc_server = None
client = None


def start_osc_server(ip, port):
    global osc_server
    osc_server = OscServer(ip, port, client)
    # Run the server in a separate thread
    osc_server_thread = threading.Thread(target=osc_server_thread_target, args=(osc_server,))
    osc_server_thread.start()      


def osc_server_thread_target(osc_server):
    """Function to run the OSC server in a separate thread."""
    osc_server.run_forever()


def connect_mixer():
    global client
    config = configuration["soundcraft"]
    client = Mixer(config["version"], config["ip"], config["port"])
    client.run_forever()


def signal_handler(signum, frame):
    print(f"Signal {signum} received.")
    dispose()


def dispose():
    global client
    if client:
        client.exit_event.set()
        client.terminate()

    global osc_server
    if osc_server:
        osc_server.terminate()


def main(args=None):
    signal.signal(signal.SIGINT, signal_handler)
    try:
        connect_mixer()
        osc = configuration["osc"]
        start_osc_server(osc["ip"], osc["listen_port"])
        signal.pause()
    except socket.timeout:
        print("SoundCratf disconnected.")
        dispose()
    except Exception as ex:
        print(ex)
        dispose()
    finally:
        print("All services disposed.")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
