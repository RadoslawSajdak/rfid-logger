import RPi.GPIO as GPIO
import time
import Logger as nfc

state = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def interrupt_handler(channel):
    global state

    print("interrupt handler")

    if channel == 16:
        if state == 0:
            state = 1
            print("state reset by event on pin 19")





if __name__ == "__main__":

    nfc.setup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    while True:
        print("Read")
        nfc.read_once()
        print(1)
        GPIO.wait_for_edge(16, GPIO.FALLING)
        print(2)
        nfc.loop()
        print(3)
        time.sleep(1)