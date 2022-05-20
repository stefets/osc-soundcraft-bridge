import time
import threading
import socket

class SoundCraftClient(object):
    def __init__(self, version, ip, port):
        self.ip = ip
        self.port = port
        self.version = version

        self.connected = False
        
        self.exit_event = threading.Event()

        self.alive_thread = threading.Thread(target=self.keep_alive_thread, args=())
        self.recv_thread = threading.Thread(target=self.receive_thread, args=())

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5.0)

    def run_forever(self):
        try:   
            self.client.connect((self.ip, self.port))
            self.client.send(b"GET /raw HTTP1.1\n\n")
            self.send_alive(0)
            print('Client connected to SoundCraft')
            self.connected = True
        except OSError as ex:
            if ex.errno == 113:
                print(f"Unable to reach {self.ip} address")
            else:
                print('Unexpected error: % d', ex.errno)
        except Exception as ex:
            print('Unexpected error: % d', ex.errno)
                
        if self.connected:
            self.alive_thread.start()
            self.recv_thread.start()
        else:
            print("ERROR : Mixer not connected.")

    def terminate(self):
        if self.alive_thread.is_alive():
            self.alive_thread.join()
        if self.recv_thread.is_alive():
            self.recv_thread.join()
        try:
            self.client.close()
            if self.connected:
                print('Disconnected from SoundCraft gracefully.')
        except:
            print("Oups")

    def mix(self, channel, value, kind='i'):
        # Mix input by default or kind
        cmd = f'SETD^{kind}.{channel}.mix^{value}\n'.encode('UTF-8')
        self.client.send(cmd)

    def imix(self, channel, value):
        # Mix input
        mix(channel,value)

    def pmix(self, channel, value):
        # Mix player
        mix(channel,value,'p')

    def lmix(self, channel, value):
        # Mix line
        mix(channel,value,'l')

    def mute(self, channel, value, kind='i'):
        # Mute input by default or kind
        cmd = f'SETD^{kind}.{channel}.mute^{value}\n'.encode('UTF-8')
        self.client.send(cmd)

    def imute(self, channel, value):
        # Mute input
        mute(channel, value)

    def pmute(self, channel, value):
        # Mute player
        self.mute(channel, value, 'p')

    def lmute(self, channel, value):
        self.mute(channel, value, 'l')


    def receive_thread(self):
        ''' Thread '''
        while True:
            try:
                if self.exit_event.is_set():
                    print("Stopping receive thread")
                    break
                ''' Sink the data for the moment '''
                _ = self.client.recv(128).decode()
            except socket.timeout:
                print('receive timeout')
                self.connected = False


    def keep_alive_thread(self):
        ''' Thread '''
        while True:
            if self.exit_event.is_set():
                print("Stopping keep_alive thread")
                break
            self.send_alive(5)


    def send_alive(self, wait=0):
        try:
            self.client.send(b"ALIVE\n")
        except socket.timeout:
            print('send_alive timeout')
            self.connected = False
            return
        time.sleep(wait)