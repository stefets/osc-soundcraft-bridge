#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import json
import signal
import socket
import warnings
import threading

from services.soundcraft import Mixer


# Config file
sys.path.append(os.path.realpath('.'))
with open('config.json') as json_file:
    configuration = json.load(json_file)
    
backends = ["python-osc", "pyliblo"]

osc_server = None
client = None


def start_osc_server(backend, ip, port):
    if backend == "pyliblo":
        use_pyliblo(port)
    elif backend == "python-osc":
        use_python_osc(ip, port)
    else:
        raise Exception(f"Unsupported backend: [{backend}]")


def use_pyliblo(port):
    global osc_server
    warnings.warn(
        "Warning: pyliblo support will not evolve further. Consider using python-osc for future compatibility.",
        DeprecationWarning, 2)
    from services.osc import OscServer
    osc_server = OscServer(port, client)
    osc_server.run_forever()


def use_python_osc(ip, port):
    global osc_server
    from services.py_osc import OscServer
    osc_server = OscServer(ip, port, client)
    # Run the server in a separate thread
    server_thread = threading.Thread(target=run_server, args=(osc_server,))
    server_thread.start()      


def run_server(server):
    """Function to run the OSC server in a separate thread."""
    server.run_forever()


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
        start_osc_server(osc["backend"], osc["ip"], osc["listen_port"])
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
