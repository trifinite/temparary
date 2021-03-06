from pybleno import *
import array
from Tesla import *

class VersionInfoCharacteristic(Characteristic):
    
    def __init__(self, tesla):
        Characteristic.__init__(self, {
            'uuid': '00000214b2d143f09b88960cebf8b91e',
            'properties': ['read'],
            'descriptors': [
                    Descriptor({
                        'uuid': '2901',
                        'value': bytes('Version Info','ascii')
                        }
                    )],   
            'value': None
          })
          
        self.tesla = tesla
          
    def onReadRequest(self, offset, callback):
        
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        else:
            data = array.array('B', [0] * 1)
            writeUInt8(data, self.tesla.crust, 0)
            callback(Characteristic.RESULT_SUCCESS, data);

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) != 1:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            pass