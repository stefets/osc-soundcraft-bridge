
import liblo

class OscServer(liblo.ServerThread):
    def __init__(self, listen_port, mixer):
        liblo.ServerThread.__init__(self, listen_port)

        self.mixer = mixer


    @liblo.make_method('/mix', None)
    def mix_callback(self, path, args):
        self.mixer.mix(args[0], args[1])

    
    @liblo.make_method('/lmix', None)
    def lmix_callback(self, path, args):
        self.mixer.mix(args[0], args[1], "l")

    
    @liblo.make_method('/pmix', None)
    def pmix_callback(self, path, args):
        self.mixer.mix(args[0], args[1], "p")


    @liblo.make_method('/mute', None)
    def mute_callback(self, path, args):
        self.mixer.mute(args[0], args[1])


    @liblo.make_method('/lmute', None)
    def lmute_callback(self, path, args):
        self.mixer.mute(args[0], args[1], "l")

    
    @liblo.make_method('/pmute', None)
    def pmute_callback(self, path, args):
        self.mixer.mute(args[0], args[1], "p")

    def terminate(self):
        self.stop()


    def run_forever(self):
        self.start()