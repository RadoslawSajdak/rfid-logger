#import RPi.GPIO as GPIO
import time
import Logger as nfc
import Database as database
import GUI as app
import threading

#TODO: Data validation (number and index len, formats etc.)

def check_item(MAC):
    """ Look for item in database and take an action.
    As input you should put MAC of item in format "aaaaaaaa" or "aa:aa:aa:aa".

    If any errors occur during reading database, "ERROR" will be printed but in app
    nothing will happen.
    """
    status = database.get_status(MAC)
    app.nfc_detection(status)
    
    # if status == "NOT_AVAILABLE":
    #     print("SWITCH_TO_RETURN_SCREEN")
    #     person, item = database.get_order(MAC)
    #     print(person,"\n",item)

    # elif status == "AVAILABLE":
    #     print("SWITCH_TO_RENT_SCREEN")
    #     date = input("Date of return: yyyy-mm-dd")
    #     database.rent_item(database.check_mac(MAC),date)

    # elif status == "NOT_PRESENT":
    #     print("SWITCH_TO_ADD_SCREEN")
    #     database.add_item(database.check_mac(MAC),name = input())
    #     app.Not_exist_window.mac = 'nowy'
    # else:
    #     print("ERROR")    

def app_thread():
    while True:
        
        #nfc.read_once()
        #database.MAC_db = input()
        #GPIO.wait_for_edge(16, GPIO.FALLING)
        scanned_MAC = nfc.loop(True)
        if app.sm.current == "main_screen":
            print(app.sm.current)
            database.MAC_db = scanned_MAC
            check_item(database.MAC_db)
            time.sleep(1)
        elif app.sm.current == "renting_screen":
            print(app.sm.current)
            database.MAC_user = scanned_MAC
            time.sleep(1)


if __name__ == "__main__":
    nfc.setup()
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    thrd = threading.Thread(target=app_thread)
    thrd.start()
    
    app.RFID_LoggerApp().run()


