print("Hello world!")

from pn532pi import Pn532Spi,Pn532, pn532
import time
#import binascii
import atexit

PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
nfc = Pn532(PN532_SPI)

def setup():
    nfc.begin() 
    time.sleep(1)
    a = nfc.getFirmwareVersion() #Check if device is working well TODO: protection like try/except
    time.sleep(1)
    print("Firmware version: ",(a >> 16) & 0xFF,".",(a >> 8) & 0xFF)
    nfc.setPassiveActivationRetries(0xFF)
    time.sleep(1)
    nfc.SAMConfig()
    time.sleep(1)
    # If all is good, setup is done
    print("Waiting for a card...\n\n")

# Reading in infinite loop
def loop():
    time.sleep(1)
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
##################### End of RFID functions ###############################
def write_to_base(string_to_write):
    f = open('/home/pi/Desktop/RFID_Logger_Telephoners/rfid-logger/Base.txt', "a")
    f.write((string_to_write + '\n'))
    f.close()

def exit_handler():
    print("Interrupted! Leaving program!")


if __name__ == '__main__':
    
    setup()
    atexit.register(exit_handler)
    while 1:
        found = loop()
        write_to_base(found)
        time.sleep(0.3)
