# osc-soundcraft-bridge
A bridge between the OSC protocol and the SoundCraft UI series.
I am disappointed of SoundCraft with the lack of updates/news for this series. It look like a 'product destinated to death' for unknown reason.

# Presentation
It's a Python service possessed by few 😈😈
* An OSC server.
* A client connected to a SoundCraft UI server through a socket.
* When an OSC message arrives, the OSC server calls the corresponding function of the SoundCraft client with the expected parameters.


<img src="/doc/osc-soundcraft-bridge.png" />


# Features to date
* Mix and mute control for all channels, line in and player
* Reverb, delay, chorus and room for all channels, line in and player
* Easy EQ : BASS, MID, TREBLE for all channels, line in and player
* Master mix volume and master record (UI12/UI16, not tested on a UI24 because its multitrack)

# Dependencies
* apt-get install liblo-dev
* pip install pyliblo

# Example
* Open the UI in a browser to see live change
* Edit the config.json file according your setup
* Start the service $python app.py
* Use your favorite OSC client, in this example I will use yoggy/sendosc
* ./sendosc 127.0.0.1 56419 /mix i 0 f 0.5
* ./sendosc 127.0.0.1 56419 /mute i 0 i 1
* ./sendosc 127.0.0.1 56419 /mute i 0 i 0
* Look at your browser to see the changes live

# Demonstration 🎥
* Part 1 : Control the SoundCraft from command line https://www.youtube.com/watch?v=seUjRcMgsTw
* Part 2 : Control the SoundCraft with a MIDI keyboard 🎹 https://www.youtube.com/watch?v=IfXxfmwl2v0
* Part 3 : In progress ( Demo with the Akai MIDI Mix and MPK 249 controllers )

# Motivation 🤔
When I play music and I want to change, for instance, the volume of an input I do it on a browser. On my PC or tablet in fact. Near everytime, my PC/tablet are in sleep mode, I have to 'awake' it, wait for the UI to come up and then I can change the volume.

This little detail is a recursive PITA that makes me near crazy++ 😫

# ENOUGH IS ENOUGH 😡
The wait is over, I want to control my SoundCraft with OSC, and ANY programs and ANY MIDI instruments/controllers 🎹 at my fingertips. 

RIGHT NOW ! 🥴

I then wrote this bridge. 🤓

# The Holy Grail 🎥
* It would have been impossible for me to make this bridge without this reference.
* https://www.youtube.com/watch?v=d0QktirWbRI
 
