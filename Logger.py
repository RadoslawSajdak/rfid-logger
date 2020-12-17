print("Hello world!")

from pn532pi import Pn532Spi,Pn532, pn532
import time
import binascii

PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
nfc = Pn532(PN532_SPI)

def setup():
    nfc.begin() 
    time.sleep(5)
    a = nfc.getFirmwareVersion() #Check if device is working well TODO: protection like try/except
    time.sleep(1)
    print("Firmware version: ",(a >> 16) & 0xFF,".",(a >> 8) & 0xFF)
    nfc.setPassiveActivationRetries(0xFF)
    time.sleep(5)
    nfc.SAMConfig()
    time.sleep(5)
    # If all is good, setup is done
    print("Waiting for a card...\n\n")


def loop():
    time.sleep(1)
    while(1):
        success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
        if (success):
            print("Card found!", uid)
            return uid

if __name__ == '__main__':
    setup()
    found = loop()

    while 1:
        found = loop()
        time.sleep(0.3)
