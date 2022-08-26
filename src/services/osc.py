import liblo

class OscServer(liblo.ServerThread):
    def __init__(self, listen_port, mixer):
        liblo.ServerThread.__init__(self, listen_port)

        self.mixer = mixer


    @liblo.make_method('/mix', None)
    def mix_callback(self, path, args):
        self.mixer.mix(args[0], args[1])

    
    @liblo.make_method('/lmix', None)
    def line_in_mix_callback(self, path, args):
        self.mixer.mix(args[0], args[1], "l")

    
    @liblo.make_method('/pmix', None)
    def player_mix_callback(self, path, args):
        self.mixer.mix(args[0], args[1], "p")

    
    @liblo.make_method('/master', None)
    def master_mix_callback(self, path, args):
        self.mixer.master(args[0])


    @liblo.make_method('/mute', None)
    def mute_callback(self, path, args):
        self.mixer.mute(args[0], args[1])


    @liblo.make_method('/lmute', None)
    def line_in_mute_callback(self, path, args):
        self.mixer.mute(args[0], args[1], "l")

    
    @liblo.make_method('/pmute', None)
    def player_mute_callback(self, path, args):
        self.mixer.mute(args[0], args[1], "p")

    
    def terminate(self):
        self.stop()


    def run_forever(self):
        self.start()