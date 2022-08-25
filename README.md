# osc-soundcraft-bridge
A bridge between the OSC protocol and the SoundCraft UI series.

NOTICE : This is, and will be for a long time an experimental bridge, tested with a version 16. Yous should fork it to create your own logic. It's NOT a production service for you because of it's garbage in / garbage out passivity.

Except for me, I use it in a production environment. Why ? Because my OSC client don't send 💩🧻🚽 to the bridge.

# Presentation
It's a Python service possessed by few 😈😈
* An OSC server.
* A client connected to a SoundCraft UI server through a socket.
* When an OSC message arrives, the OSC server calls the corresponding function of the SoundCraft client with the expected parameters.

# Dependencies
* apt-get install liblo-dev
* pip install pyliblo

# Example
* Open the UI in a browser to see live change
* Edit the config.json file according your setup
* Start the service $python bridge.py
* Use your favorite OSC client, in this example I will use yoggy/sendosc
* ./sendosc 127.0.0.1 56419 /mix i 0 f 0.5
* ./sendosc 127.0.0.1 56419 /mute i 0 i 1
* ./sendosc 127.0.0.1 56419 /mute i 0 i 0
* Look at your browser to see the changes live

# Demonstration 🎥
* Control the SoundCraft from command line https://www.youtube.com/watch?v=seUjRcMgsTw
* Control the SoundCraft with a MIDI keyboard 🎹 https://www.youtube.com/watch?v=IfXxfmwl2v0

# Motivation 🤔
When I play music and I want to change, for instance, the volume of an input I do it on a browser. On my PC or tablet in fact. Near everytime, my PC/tablet are in sleep mode, I have to 'awake' it, wait for the UI to come up and then I can change the volume.

This little detail is a recursive PITA that makes me near crazy++ 😫

# ENOUGH IS ENOUGH 😡
The wait is over.

I want to control my SoundCraft with OSC, and ANY programs and ANY MIDI instruments/controllers 🎹 at my fingertips. 

RIGHT NOW ! 🥴

I then wrote this bridge. 🤓

# The Holy Grail 🎥
* It would have been impossible for me to make this bridge without this reference.
* https://www.youtube.com/watch?v=d0QktirWbRI
 
