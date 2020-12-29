import RPi.GPIO as GPIO
import time
import Logger as nfc
import Database as database
import rfid_scan as app
import threading


def check_item(MAC):
    """ Look for item in database and take an action.
    As input you should put MAC of item in format "aaaaaaaa" or "aa:aa:aa:aa".

    If any errors occur during reading database, "ERROR" will be printed but in app
    nothing will happen.
    """
    status = database.get_status(MAC)
    print(MAC, status)
    if status == "NOT_AVAILABLE":
        print("SWITCH_TO_RETURN_SCREEN")
        person, item = database.get_order()
        print(person,"\n",item)

    elif status == "AVAILABLE":
        print("SWITCH_TO_RENT_SCREEN")
        date = input("Date of return: yyyy-mm-dd")
        database.rent_item(database.check_mac(MAC),date)

    elif status == "NOT_PRESENT":
        print("SWITCH_TO_ADD_SCREEN")
        database.add_item(database.check_mac(MAC),name = input())

    else:
        print("ERROR")    

def app_thread():
    while True:
        print("Read")
        nfc.read_once()
        GPIO.wait_for_edge(16, GPIO.FALLING)
        check_item(nfc.loop())
        time.sleep(1)


if __name__ == "__main__":
    nfc.setup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    thrd = threading.Thread(target=app_thread)
    thrd.start()
    #app.RFIDApp().run()


