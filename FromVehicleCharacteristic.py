import threading
from time import sleep
from pybleno import *

from Tesla import bcolors, getOutputStringFV

class FromVehicleCharacteristic(Characteristic):
    
    def __init__(self, tesla):
        Characteristic.__init__(self, {
            'uuid': '00000213b2d143f09b88960cebf8b91e',
            'properties': ['indicate'],
            'descriptors': [
                    Descriptor({
                        'uuid': '2901',
                        'value': bytes('From Vehicle','ascii')
                        })],   
            'value': None
          })
        self.tesla = tesla
        threading.Thread(None,self.watchMessage).start()
        self._updateValueCallback = None
            
    def watchMessage(self):
        sleep(0.5)
        if (len(self.tesla.messagelist)>0):
            try:
                msg = self.tesla.messagelist.pop(0)
                self._updateValueCallback(msg)
                print(bcolors.OKGREEN+"Sent Message:\n"+getOutputStringFV(msg,self.tesla.human)+bcolors.ENDC)
            except Exception as e:
                print('... '+str(e))

        if threading.main_thread().isAlive():
            threading.Thread(None,self.watchMessage).start()

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print("onSubscribe")
        self._updateValueCallback = updateValueCallback        
        return super().onSubscribe(maxValueSize, updateValueCallback)
            
    def onUnsubscribe(self):
        print('EchoCharacteristic - onUnsubscribe');
        self._updateValueCallback = None
