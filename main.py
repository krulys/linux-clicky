#!/usr/bin/env python3
from pynput import keyboard
from os import listdir, getcwd, system
from random import choice
from linux_clicky.play_sound import PlaySound
from optparse import OptionParser
from signal import signal, SIGINT
from sys import exit

# Handle CTRL+C
def signal_handler(signal, frame):
    system("stty echo")
    print ('\033[1;32mCTRL + C Detected. Exiting ...')
    print ('Ignore any errors after this message.\033[1;m')
    exit(0)
signal(SIGINT, signal_handler)

# Handle arguments
parser = OptionParser()
parser.add_option(
    '-v', '--volume', action="store", dest='volume',
    help="sets the volume of the clicks, anything above 1 will increase the " +
    "volume, and anything less will decrease it. Don't use numbers bigger " +
    "than 2")

parser.set_defaults(volume=1)
(options, args) = parser.parse_args()

sounds = listdir(getcwd() + '/sounds')
sound_tmp = {}
sound_tmp["click"] = []
for sound in sounds:
    if sound == 'enter.wav':
        sound_tmp["enter"] = sound
    elif sound == 'space.wav':
        sound_tmp["space"] = sound
    else:
        sound_tmp["click"].append(sound)
sounds = sound_tmp

# Volume: Negative to lower the volume
volume = str(options.volume)

key_sound_pair = dict()
honkRegistry = []
doHonk = False
system("clear")
system("stty -echo")
def on_press(key):
    try:
        global doHonk, honkRegistry,key_sound_pair,volume
        #Regular keys
        
        key_sound_pair[key.char.lower()] = choice(sounds["click"])
        filename = getcwd() + '/sounds/' +\
                        key_sound_pair[key.char.lower()]
        #Detect honk
        if key.char.lower() == "h" and honkRegistry == []:
            honkRegistry.append(key.char.lower())
        
        elif key.char.lower() == "o" and honkRegistry == ["h"]:
            honkRegistry.append(key.char.lower())
            
        elif key.char.lower() == "n" and honkRegistry == ["h","o"]:
            honkRegistry.append(key.char.lower())
        
        elif key.char.lower() == "k" and honkRegistry == ["h","o","n"]:
            doHonk = not doHonk
            honkRegistry.clear()
        else:
            honkRegistry.clear()
        
        #Do honk
        if doHonk:
            PlaySound(filename, volume).start()
    except AttributeError:
        #Special Keys
        
        if hasattr(key, "enter") and key == key.enter:
            filename = getcwd() + '/sounds/' + sounds["enter"]
        else:
            filename = getcwd() + '/sounds/' + sounds["space"]
            
        if doHonk:
            PlaySound(filename, volume).start()
        

while True:
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()
        
        
