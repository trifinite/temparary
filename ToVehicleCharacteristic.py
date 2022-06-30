from pybleno import *
import array
import struct
import sys
import traceback
from builtins import str

from Tesla import bcolors, getOutputStringTV

class ToVehicleCharacteristic(Characteristic):
    
    def __init__(self, tesla):
        Characteristic.__init__(self, {
            'uuid': '00000212b2d143f09b88960cebf8b91e',
            'properties': ['write'],
            'descriptors': [
                    Descriptor({
                        'uuid': '2901',
                        'value': bytes('To Vehicle','ascii')
                        })],   
            'value': None
          })
          
        self.tesla = tesla
          
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        print(bcolors.OKBLUE+"Received Message:\n"+getOutputStringTV(data,self.tesla.human)+bcolors.ENDC)
        self.tesla.handleMessage(data)
        callback(Characteristic.RESULT_SUCCESS);
