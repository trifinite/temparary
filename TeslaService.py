from pybleno import *
from ToVehicleCharacteristic import *
from FromVehicleCharacteristic import *
from VersionInfoCharacteristic import *

class TeslaService(BlenoPrimaryService):
    def __init__(self, tesla):
        BlenoPrimaryService.__init__(self, {
          'uuid': '00000211B2D143F09B88960CEBF8B91E',
          'characteristics': [
            ToVehicleCharacteristic(tesla),
            FromVehicleCharacteristic(tesla),
            VersionInfoCharacteristic(tesla)
          ]})
