<a href="https://trifinite.org/stuff/tempara/" target="_blank"><img align="right" src="/images/temparary_logo.png"/></a>

# temparary - Emulate the BLE interface of Tesla Vehicles
This tool is part of Project TEMPA (https://trifinite.org/tempa/)

Find out more about the temparary application on https://trifinite.org/stuff/temparary/ 

## About
Modern Tesla vehicles (Model 3, Model Y, Model S (2021+) and Model X (2021+)) have a feature where the owner's smartphone can be used as car key. In order to make this work, each Tesla vehicle is exposing a Bluetooth LE interface that is used for passing messages to the phone and to receive messages from the connected phone.

The Tesla research conducted by trifinite.org has shown, that the trust model of the Tesla "Phone-as-a-key" is very unbalanced. Where the smartphone has to cryptographically prove its identity to the vehicle for most of the security-relevant functions, the vehicle itself does not have to do so. Therefore, attackers are able to emulate a Tesla vehicle's Bluetooth interface and communicate to smartphones that connect to the emulated vehicle.

The temparary tool can impersonate/emulate a Tesla car. For the tool to impersonate a specific vehicle in question, the temparary tool requires information that is recognized by the smartphone.

The required information consist of:
* an Extended Inquiry Response dataset, that encodes properties of an iBeacon
* a Scan Response thar encodes the Vehicle ID (S<8 bytes that are hex-encoded>C)
* the Bluetooth device address (MAC-address)
* the vehicles public key

The temparary-profiler tool (https://github.com/trifinite/temparary-profiler) is able to retrieve this information from the actual vehicle.

## Installation
Install all the reqiuired python requiremets: (install packages as root)
```
#> python3 -m pip install -r requirements.txt
```

## Usage
Since the used pybleno library (https://github.com/Adam-Langley/pybleno) is not getting along well with the default bluetooth service on many linux systems, please make sure to stop the bluetooth service (in case it is started by default). Also, the pybleno library is directly talking to the HCI interface and therefore needs certain permissions. Therefore, these commands require root privileges.

Before you start, edit your copy of the temparary.py script and adjust 

This works for Ubuntu:
```
#> systemctl stop bluetooth
```

Next to the victim smartphone run: (as root)
```
#> python3 temparary.py <name of profile.json>
```


* use the bluez-tool `bdaddr` in order to set your Bluetooth interface to the addreesss of your vehicle. The Android app is capable of determining the MAC address of your vehicle and only will connect if this is correct.
* make sure to stop and/or disable your system's bluetoothd process, as it interferes with temparary's BLE advertisement
* copy the `exapmle_vehicle.json` file and adjust the values to the ones that the vehicle that is going to be impersonated is using.

### Key-Drop Attack
* wait for the smart phone app to connect to your temparary session.
* toggle the keydrop bit by entering 'k' followed by the return key
* request an authorization response by entering 'a' followed by the return key
* see the device disconnecting
* exit the application by entering 'q' followed by the return key

### Crypto Counter Confusion / Rolling Key Attack
* wait for the smart phone app to connect to your temparary session.
* toggle the phone bit by entering 'p' followed by the return key until the right phone type is displayed (Adndroid or iPhone)
* toggle the cryptocounter bit by entering 'c' followed by the return key
* request an authorization response by entering 'a' followed by the return key
* see how the message id is now 
* exit the application by entering 'q' followed by the return key


## Disclaimer
Only use this tool on Tesla vehicles and smartphones you own or have permission to do so!
