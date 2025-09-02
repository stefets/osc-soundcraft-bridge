# osc-soundcraft-bridge
A bridge between the OSC protocol and the SoundCraft UI series.

- **Tested on an UI16**

### A Python API possessed by two daemons
* 😈 An OSC server exposing paths and expecting precise args.
* 😈 A client socket connected to your SoundCraft UI server.

### Supported UI features (Tested on UI16)
* Master Mix
* Toggle record
* Mix and mute for all channels, line in and player
* Mix for reverb, delay, chorus and room for all channels, line in and player
* Easy EQ : BASS, MID, TREBLE for all channels, line in and player
* AuxSends
  * Mix for each Aux
  * Aux Send for all channels for a specific Aux

### Dependencies
  * pip install python-osc

### Example
* Open the UI in a browser to see live change
* Edit the config.json file according your setup
* Start the service $python app.py
* Use your favorite OSC client, in this example I will use yoggy/sendosc
* ./sendosc 127.0.0.1 56419 /mix i 0 f 0.5
* ./sendosc 127.0.0.1 56419 /mute i 0 i 1
* ./sendosc 127.0.0.1 56419 /mute i 0 i 0
* Look at your browser to see the changes live

### Motivation 🤔
When I play music and I want to change, for instance, the volume of an input I do it on a browser. On my PC or tablet in fact. Near everytime, my PC/tablet are in sleep mode, I have to 'awake' it, wait for the UI to come up and then I can change the volume.

This little detail is a recursive PITA that makes me near crazy++ 😫

### ENOUGH IS ENOUGH 😡
The wait is over, I want to control my SoundCraft with OSC, and ANY programs and ANY MIDI instruments/controllers 🎹 at my fingertips. 

RIGHT NOW ! 🥴

I then wrote this bridge. 🤓

### The Holy Grail 🎥
* It would have been impossible for me to make this bridge without this reference.
* https://www.youtube.com/watch?v=d0QktirWbRI
 
