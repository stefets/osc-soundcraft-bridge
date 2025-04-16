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
from exceptions import GracefulExit


# Config file
sys.path.append(os.path.realpath('.'))
with open('config.json') as json_file:
    configuration = json.load(json_file)
    

osc_server = None
client = None


def run_osc_server():
    global osc_server
    osc = configuration["osc"]
    osc_server = OscServer(osc["ip"], osc["listen_port"], client)
    # Run the server in a separate thread
    osc_server_thread = threading.Thread(target=osc_server_thread_target, args=(osc_server,))
    osc_server_thread.start()      


def osc_server_thread_target(osc_server):
    """Function to run the OSC server in a separate thread."""
    osc_server.run_forever()


def connect_to_mixer():
    global client
    config = configuration["soundcraft"]
    client = Mixer(config["version"], config["ip"], config["port"])
    client.run_forever()


def signal_handler(signum, frame):
    raise GracefulExit(f"Received signal {signum}")


def dispose():
    global client
    global osc_server

    print("Cleaning up...")
    
    if client:
        client.exit_event.set()
        client.terminate()
    
    if osc_server:
        osc_server.terminate()

    print("All services disposed.")


def main(args=None):
    signal.signal(signal.SIGINT, signal_handler)
    try:
        connect_to_mixer()
        run_osc_server()
        signal.pause()
    except socket.timeout as st:
        print("socket timeout: Soundcraft server connection lost - stopping service.")
    except GracefulExit as ge:
        print(f"Graceful exit: {ge}")        
    except Exception as ex:
        print(f"Fatal error: {ex}")
    finally:
        dispose()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
