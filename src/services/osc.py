import liblo

class OscServer(liblo.ServerThread):
    def __init__(self, listen_port, mixer):
        liblo.ServerThread.__init__(self, listen_port)

        self.mixer = mixer


    @liblo.make_method('/mix', None)
    def mix_callback(self, path, args):
        self.mixer.mix(args[0], args[1], args[2])

    
    @liblo.make_method('/master', None)
    def master_mix_callback(self, path, args):
        self.mixer.master(args[0])


    @liblo.make_method('/mute', None)
    def mute_callback(self, path, args):
        self.mixer.mute(args[0], args[1], args[2])


    @liblo.make_method('/reverb', None)
    def fx_mix_reverb_callback(self, path, args):
        self.mixer.fx(args[0], args[1], args[2], 0)

    
    @liblo.make_method('/delay', None)
    def fx_mix_delay_callback(self, path, args):
        self.mixer.fx(args[0], args[1], args[2], 1)

    
    @liblo.make_method('/chorus', None)
    def fx_mix_chorus_callback(self, path, args):
        self.mixer.fx(args[0], args[1], args[2], 2)

    
    @liblo.make_method('/room', None)
    def fx_mix_room_callback(self, path, args):
        self.mixer.fx(args[0], args[1], args[2], 3)

    
    @liblo.make_method('/rectoggle', None)
    def master_mix_record_callback(self, path, args):
        self.mixer.record()

    
    @liblo.make_method('/bass', None)
    def easy_eq_bass_callback(self, path, args):
        self.mixer.easy_eq(args[0], args[1], args[2], 1)

    
    @liblo.make_method('/mid', None)
    def easy_eq_mid_callback(self, path, args):
        self.mixer.easy_eq(args[0], args[1], args[2], 2)


    @liblo.make_method('/treble', None)
    def easy_eq_treble_callback(self, path, args):
        self.mixer.easy_eq(args[0], args[1], args[2], 3)


    def terminate(self):
        self.stop()


    def run_forever(self):
        self.start()