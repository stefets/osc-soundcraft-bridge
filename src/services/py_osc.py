#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

class OscServer():
    def __init__(self, ip, port, mixer):
        self.mixer = mixer
        
        self.dispatcher = Dispatcher()
        self.create_map()
        self.dispatcher.set_default_handler(self.default_handler)
        
        self.server = BlockingOSCUDPServer((ip, port), self.dispatcher)

    def create_map(self):
        self.dispatcher.map("/mix", self.mix_callback)
        self.dispatcher.map("/mute", self.mute_callback)
        self.dispatcher.map("/master", self.master_mix_callback)
        
        self.dispatcher.map("/room/mute", self.mix_chorus_mute_callback)
        self.dispatcher.map("/delay/mute", self.mix_delay_mute_callback)
        self.dispatcher.map("/chorus/mute", self.mix_chorus_mute_callback)
        self.dispatcher.map("/reverb/mute", self.mix_reverb_mute_callback)
        
        self.dispatcher.map("/room", self.fx_mix_room_callback)
        self.dispatcher.map("/delay", self.fx_mix_delay_callback)
        self.dispatcher.map("/chorus", self.fx_mix_chorus_callback)
        self.dispatcher.map("/reverb", self.fx_mix_reverb_callback)
        
        self.dispatcher.map("/rectoggle", self.master_mix_record_callback)
        
        self.dispatcher.map("/bass", self.easy_eq_bass_callback)
        self.dispatcher.map("/mid", self.easy_eq_mid_callback)
        self.dispatcher.map("/treble", self.easy_eq_treble_callback)
                
    def default_handler(self, path, *args):
        print(("DEFAULT " + path + ":" + "{}".format(args)))
        
    def master_mix_callback(self, path, args):
        self.mixer.master(args)    
    
    def mix_callback(self, path, *args):
        self.mixer.mix(args[0], args[1], args[2])
        
    def mute_callback(self, path, *args):
        self.mixer.mute(args[0], args[1], args[2])
        
    def mix_reverb_mute_callback(self, path, *args):
        self.mixer.fx_mute(args[0], args[1], args[2], 0)
        
    def mix_delay_mute_callback(self, path, *args):
        self.mixer.fx_mute(args[0], args[1], args[2], 1)
        
    def mix_chorus_mute_callback(self, path, *args):
        self.mixer.fx_mute(args[0], args[1], args[2], 2)
        
    def mix_room_mute_callback(self, path, *args):
        self.mixer.fx_mute(args[0], args[1], args[2], 3)          
        
    def fx_mix_reverb_callback(self, path, *args):
        self.mixer.fx(args[0], args[1], args[2], 0)

    def fx_mix_delay_callback(self, path, *args):
        self.mixer.fx(args[0], args[1], args[2], 1)

    def fx_mix_chorus_callback(self, path, *args):
        self.mixer.fx(args[0], args[1], args[2], 2)

    def fx_mix_room_callback(self, path, *args):
        self.mixer.fx(args[0], args[1], args[2], 3)
        
    def master_mix_record_callback(self, path, args):
        self.mixer.record()

    def easy_eq_bass_callback(self, path, *args):
        self.mixer.easy_eq(args[0], args[1], args[2], 1)
    
    def easy_eq_mid_callback(self, path, *args):
        self.mixer.easy_eq(args[0], args[1], args[2], 2)

    def easy_eq_treble_callback(self, path, *args):
        self.mixer.easy_eq(args[0], args[1], args[2], 3)

    def terminate(self):
        print("Stopping OSC Server")
        self.server.shutdown()
        self.server.server_close()
        print("Server stopped")

    def run_forever(self):
        print("Starting OSC Server")
        self.server.serve_forever()  # Blocks forever
