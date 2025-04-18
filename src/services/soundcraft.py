import time
import threading
import socket

class Mixer(object):
    def __init__(self, version, ip, port, dry_run=False):
        self.ip = ip
        self.port = port
        self.version = version

        self.connected = False
        self.dry_run = dry_run
        
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
            print("Abnormal termination")


    def master(self, value):
        cmd = f'SETD^m.mix^{value}\n'
        self.send_packet(cmd)
        

    def mix(self, channel, value, kind):
        self.send_packet(f'SETD^{kind}.{channel}.mix^{value}\n')


    def mute(self, channel, value, kind):
        self.send_packet(f'SETD^{kind}.{channel}.mute^{value}\n')

    
    def fx(self, channel, value, kind, index):
        '''
            For index, 0:reverb, 1:delay, 2:chorus, 3:room
        '''
        self.send_packet(f'SETD^{kind}.{channel}.fx.{index}.value^{value}\n')


    def fx_mute(self, input, value, datatype, fx_index):
        '''
            For index, 0:reverb, 1:delay, 2:chorus, 3:room
        '''
        self.send_packet(f'SETD^{datatype}.{input}.fx.{fx_index}.mute^{value}\n')


    def record(self):
        self.send_packet(f"RECTOGGLE\n")


    def easy_eq(self, channel, value, kind, index):
        '''
            For index, 1:BASS, 2:MID, 3:TREBLE
        '''
        self.send_packet(f'SETD^{kind}.{channel}.eq.b{index}.gain^{value}\n')


    def aux_send(self, channel, value, aux_index):
        '''
            For aux_index, 0:aux1, 1:aux2, 2:aux3, 3:aux4, 4:aux5
        '''
        self.send_packet(f'SETD^i.{channel}.aux.{aux_index}.value^{value}\n')


    def send_packet(self, command):
        self.client.send(command.encode("UTF-8")) if not self.dry_run else print(command)


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