#!/usr/bin/env python3

import json
from re import I
from pybleno import *
import sys
import signal
from Tesla import *
from TeslaService import *
import pyfiglet

__author__ = "Martin Herfurt (trifinite.org)"
__version__ = "0.1.1"
__license__ = "MIT"

ascii_banner = pyfiglet.figlet_format("temparary")
print(ascii_banner)
print("Author:  "+__author__)
print("Version: "+__version__+"\n")

configfile=''
try:
    configfile = sys.argv[1]
except:
    configfile=''

if (len(configfile)<4):
    print("No config file. Exiting")
    exit(0)

config = {
    "eir": "0201061aff4c00021574278bdab64445208f0c720eaf05993500002342c5", 
    "response": "030222111309533066373838356332616631613665663943", 
    "pubkeyResponse": "0025"
}

with open(configfile, 'r') as f:
    config = json.load(f)

bleno = Bleno()
name = 'S0f7885c2af1a6ef9C'
vehicleUuid = "74278BDAB64445208F0C720EAF059935"
tesla = Tesla(config)
teslaService = TeslaService(tesla)
eir = bytearray.fromhex(config['eir']) 
scanResponse = bytearray.fromhex(config['response'])


def onStateChange(state):
    if (state == 'poweredOn'):
        def on_startAdvertising(err):
            if err:
                print(err)
        bleno.startAdvertisingWithEIRData(eir, scanResponse, on_startAdvertising)
    else:
        bleno.stopAdvertising();
bleno.on('stateChange', onStateChange)

def onTest(state):
    print("Service added")

def onAccept(state):
    print("Connect from:    "+str(state))

def onDisconnect(state):
    print("Disconnect from: "+str(state))
    
def onAdvertisingStart(error):
    if not error:
        print('advertising...')
        bleno.setServices([
            teslaService
        ])

bleno.on('advertisingStart', onAdvertisingStart)
bleno.on('disconnect', onDisconnect)
bleno.on('accept', onAccept)
bleno.on('servicesSet', onTest)
bleno.start()

inkey =''
print("a : request authorization\ne : toggle evil bit\nh : toggle human bit\nq : terminate")


while (inkey != 'q'):
    if (sys.version_info > (3, 0)):
        ##input()
        inkey = sys.stdin.read(1)
    else:
        raw_input()

    if (inkey == 'a'): # request authorization from Tesla app
        tesla.messagelist.append(bytearray.fromhex('001c1a1a12160a14ffff96c0b80f5a242076ca7bdf9524e1bd78da791802'))
    elif (inkey == 'e'): # toggle evil bit
        tesla.toggleEvilBit()
        print("Evil bit: "+str(tesla.evil))
    
    elif (inkey == 'h'): # toggle evil bit
        tesla.toggleHumanBit()
        print("Human bit: "+str(tesla.human))

bleno.stopAdvertising()
bleno.disconnect()

print ('temparary has terminated.')
sys.exit(1)
