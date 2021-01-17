from pn532pi import Pn532Spi,Pn532, pn532
import time

PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
nfc = Pn532(PN532_SPI)

def setup():
    """ Init function for RFID. Should be called at the beggining of the code but just once. """
    nfc.begin() 
    time.sleep(1)
    a = nfc.getFirmwareVersion() #Check if device is working well TODO: protection like try/except
    time.sleep(1)
    while (str((a >> 16) & 0xFF) + "." + str((a >> 8) & 0xFF)) != "1.6":
        a = nfc.getFirmwareVersion() #Check if device is working well TODO: protection like try/except
        time.sleep(0.2)
    print("Firmware version: ",(a >> 16) & 0xFF,".",(a >> 8) & 0xFF)
    nfc.setPassiveActivationRetries(0xFF)
    time.sleep(1)
    error = False
    while not error:
        error = nfc.SAMConfig()

    print(error)
    
    time.sleep(1)
    # If all is good, setup is done
    print("Waiting for a card...\n\n")

def read_once():
    """ 
    Flash RFID module's memory and activate RF Field 
    
    You should call it before each interrupt!
    """
    nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

# Reading in infinite loop
def loop(infinite_wait):
    """
    Reading loop. Returns MAC in AA:AA:AA:AA format. 
    """
    ticks = 0
    while(1):
        success, uid_t = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
        if (success):
            uid = ""
            ### Conversion of byte array to string MAC string ###
            for i in uid_t:
                if i < 0x10:
                    uid += "0" + str(hex(i))
                else:
                    uid += str(hex(i))
                if len(uid) < 19: uid += ":"
            uid = uid.replace('0x','')
            uid = uid.upper()
            print("Card found!", uid)
            return uid
        else:
            ticks += 1
            time.sleep(0.01)
            if ticks > 200 and infinite_wait is False: # Maximum time of waiting for loop
                return ""


if __name__ == '__main__':
    
    setup()
    while 1:
        found = loop()

        print(found)
        time.sleep(0.3)
