<a href="https://trifinite.org/stuff/tempara/" target="_blank"><img align="right" src="/images/temparary_logo.png"/></a>

# temparary - Emulate the BLE interface of Tesla Vehicles

Find out more about the temparary application on https://trifinite.org/stuff/temparary/ 

## Disclaimer
Only use this tool on Tesla vehicles and smartphones you own or have permission to do so!

## Usage

* use the bluez-tool `bdaddr` in order to set your Bluetooth interface to the addreesss of your vehicle. The Android app is capable of determining the MAC address of your vehicle and only will connect if this is correct.

* make sure to stop and/or disable your system's bluetoothd process, as it interferes with temparary's BLE advertisement

* copy the `exapmle_vehicle.json` file and adjust the values to the ones that the vehicle that is going to be impersonated is using.

### Key drop attack

* wait for the smart phone app to connect to your temparary session.

* toggle the evil bit by entereing 'e' followed by the return key

* request an authorization by entering 'a' followed by the return key

* see the device disconnecting

* exit the application by entering 'q' followed by the return key

Check out the video in <a href="https://github.com/trifinite/temparary/blob/main/images/KeyDrop.mp4?raw=true">/images/KeyDrop.mp4</a> for a brief demonstration.
