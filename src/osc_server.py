
import liblo

class OscServer(liblo.ServerThread):
    def __init__(self, listen_port, mixer):
        liblo.ServerThread.__init__(self, listen_port)

        self.mixer = mixer

    @liblo.make_method('/mix', None)
    def mix_callback(self, path, args):
        self.mixer.mix(args[0], args[1])


    @liblo.make_method('/mute', None)
    def mute_callback(self, path, args):
        self.mixer.mute(args[0], args[1])


    def terminate(self):
        self.stop()


    def run_forever(self):
        self.start()