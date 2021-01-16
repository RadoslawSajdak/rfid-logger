from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import date, datetime
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import testy
import Database as database
from kivy.config import Config
from functools import partial ##import partial, wich allows to apply arguments to functions returning a funtion with that arguments by default.
from kivy.utils import get_color_from_hex
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

from Logger import loop


class Main_window(Screen):
    """Main window design and functionality"""

    def on_enter(self):
        """Update local values"""
        self.dev_data = database.get_all_devices()   ###FROM DATABASE: list of devices
        pass
    

    def dev_base(self):
        """Print out list of defices in our database"""
        top_button_share = 1.1
        self.ids.list.clear_widgets()

        for i in range (len(self.dev_data)):
            top_button_share -= .1
            button_share = Button(pos_hint={"x": 0, "top": top_button_share},
                            size_hint_y=None, 
                            height=40)

            spaces = 70*" "                                                 #Device information buffor
            dev_information = str(self.dev_data[i]["name"])

            if self.dev_data[i]["status"]=="AVAILABLE":
                dev_information += spaces[len(str(self.dev_data[i]["name"])): -len(str(self.dev_data[i]["status"]))]      #Set particular number of spaces to keep 70chars in line
                dev_information += str(self.dev_data[i]["status"]) 

                button_share.background_color = get_color_from_hex('#6FAF8B') 
                button_share.background_normal = ""      
                button_share.color = (0, 0, 0, 1)   

            else:
                dev_information += spaces[len(str(self.dev_data[i]["name"])): -len(str(self.dev_data[i]["return_date"]))]    
                dev_information += "    "
                dev_information += str(self.dev_data[i]["return_date"]) 
                
                button_share.background_normal = ""      
                button_share.color = (0, 0, 0, 1)  

                today = date.today()
                #Check return date and use color for it
                if today >= self.dev_data[i]["return_date"]:
                    button_share.background_color = get_color_from_hex('#FF5733') 
                else:
                    button_share.background_color = get_color_from_hex('#a6a6a6')
            
            button_callback = partial(dev_info_pop, self.dev_data[i])       #Send argument to function
            button_share.bind(on_press = button_callback)            

            button_share.text = dev_information                             #Button text == List content

            self.ids.list.add_widget(button_share)
        
    

class Renting_window(Screen):
    """Renting window design and functionality"""

    us_data = {                            #user data buffor
            "user_id" : "",
            "name" : "",
            "surname" : "",
            "student_id" : "",
            "mac" : "",
            "email" : "",
            "phone" : ""}


    def on_enter(self):
        """Get data from database and update internal variables """
        self.dev_data = database.get_one_part(database.MAC_db) 

        #clear variable
        for key in self.us_data:
            self.us_data[key] = ""

        self.fill_data()
        self.return_date.text = ""          #clear data value


    def fill_data(self):
        """Fill text input by dev_data information"""

        self.dev_name.text = self.dev_data["name"]
        self.dev_mac.text = self.dev_data["mac"]
        
        self.us_name.text = self.us_data["name"]
        self.us_surname.text = self.us_data["surname"]
        self.us_index.text = self.us_data["student_id"]
        self.us_email.text = self.us_data["email"]
        self.us_phone.text = self.us_data["phone"]


    def check_date(self):
        """Check if written data is correct (format/value bigger than today's date)
            returning if(correct)
        """
        datestr = datetime.now()
        try:
            datestr = datetime.strptime(self.return_date.text, '%Y-%m-%d')
        except:
            pass
        today = datetime.now()
        if not(datestr > today):
            invalid_time()
        return 0 if not(datestr > today) else 1


    def today(self):
        """Get actual date"""
        today = date.today()
        return today.strftime("%Y-%B-%d")


    def empty_value(self, value_type, value):
        """Check if value is empty - some information are required
            return if(not empty)
        """
        if len(value)<2:
            required_info(value_type)       #popup
        return 0 if len(value)<2 else 1
    

    def rent_button(self):
        """Rent button functionality
            Check required values - if(not empty) - name, surname, email
            Bact to main window and write data into base
        """
        self.correct = self.empty_value("Name",self.us_name.text)
        if (self.correct) :
            self.correct = self.empty_value("Surname",self.us_surname.text) 
        if (self.correct) :
            self.correct = self.empty_value("E-mail",self.us_email.text)
        if (self.correct) :
            self.correct = self.check_date() 
        if (self.correct) :
            self.renting_user={"name":self.us_name.text, \
                "surname": self.us_surname.text, \
                "student_id": self.us_index.text, \
                "email" : self.us_email.text, \
                "phone" : self.us_phone.text, \
                "return_date" : self.return_date.text, \
                "mac" : self.us_data["mac"]}
            database.rent_item(database.MAC_db, self.renting_user)

            sm.current= "main_screen"
            sm.transition.direction = "right"


    def scan_student_card_button(self):
        """Scan student card button procedure """
        self.pop = scan_student_card()                 #run popup and store its pointer 
        database.MAC_user = ""                         #clear saved MAC
        Clock.schedule_once(self.card_scanned, 5)      #5s scan timer


    def card_scanned(self, trash):
        """After scanning procedure - data acquisition"""
        self.us_data = database.get_user(database.check_mac(database.MAC_user))
        print(self.us_data)
        self.fill_data()
        self.pop.dismiss()                              #close popup


    def cancel_button(self):
        """Cancel button functionality
            return to main window
        """
        sm.current= "main_screen"
        sm.transition.direction = "right" 


class Return_window(Screen):
    """Return window design and functionality"""

    def on_enter(self):
        """Get data from database and update internal variables """
        user, part = database.get_order(database.MAC_db)
        self.user_data = user
        self.dev_data = part  
        
        self.us_name.text = self.user_data["name"]
        self.us_surname.text = self.user_data["surname"]
        self.us_index.text = self.user_data["student_id"]
        self.us_email.text = self.user_data["email"]
        self.us_phone.text = self.user_data["phone"]

        self.dev_name.text = self.dev_data["name"]
        self.dev_id.text = str(self.dev_data["part_id"])
        self.dev_mac.text = self.dev_data["mac"]

        #Set initial values
        self.return_date.text = "" 
        self.return_button_id.text = "Return"


    def today(self):
        """Return actual date"""
        today = date.today()
        return today.strftime("%Y-%B-%d")


    def check_date(self):
        """Check if written data is correct (format/value bigger than today's date)
            returning if(correct)
        """
        datestr = datetime.now()
        try:
            datestr = datetime.strptime(self.return_date.text, '%Y-%m-%d')
        except:
            pass
        today = datetime.now()
        if not(datestr > today):
            self.return_button_id.text = "Return"
            invalid_time()
        else:
            self.return_button_id.text = "Prologue"


    def return_button(self):
        """Return button procedure
            Prologue or return
            Back to main menu
        """
        if self.return_button_id.text == "Prologue":
            #Device prologue
            database.prologue(self.dev_data["part_id"], self.return_date.text )             
        else:
            #Devive returned
            database.return_item(self.dev_data["mac"])

        sm.transition.direction = "down"
        sm.current = "main_screen"


    def cancel_button(self):
        """Cancel button functionality
            return to main window
        """
        sm.transition.direction = "down"
        sm.current = "main_screen"



class Not_exist_window(Screen):
    """Not exist window design and functionality"""
    def on_enter(self):
        """Get data from database and update internal variables """
        self.dev_mac.text=database.MAC_db

    def empty_value(self, value_type, value):
        """Check if value is empty - some data are required
            return if(not empty)
        """
        if (len(value)<2 or len(value)>40) :
            required_info(value_type+ "  must be 2-40 character long")
        return 0 if (len(value)<2 or len(value)>40) else 1

    def add_button(self):
        """Add button functionality
            Check inputs and send to database
        """
        self.correct = self.empty_value("Device name", self.dev_name.text)
        if(self.correct):
            self.new_name={"name":self.dev_name.text}
            database.add_item(database.MAC_db,self.dev_name.text)
            sm.current= "main_screen"
            sm.transition.direction = "left" 

    def cancel_button(self):
        """Cancel button functionality
            return to main screen
        """
        sm.current= "main_screen"
        sm.transition.direction = "left" 



class RFID_LoggerApp(App):
    """Main aplication class - must have"""
    def build(self):
        return sm





def invalid_time():
    """Popup to tell that data is not correct"""
    box = BoxLayout()
    box.add_widget(Label(text='Please use YYYY-MM-DD format', halign = 'center'))
    pop = Popup(title='Data format incorrect',
                content=box,
                separator_height = 4,
                title_size = 19,
                size_hint=(None, None), size=(400, 300),
                background= 'kivy_img/NOT_AVAILABLE background.png')

    pop.open()

def required_info(info_name):
    """Popup to tell that information written by user is not correct"""
    box = BoxLayout()
    box.add_widget(Label(text='This information is required :\n' + info_name, halign = 'center'))
    pop = Popup(title = "Required info",
                content=box,
                separator_height = 4,
                title_size = 19,
                size_hint=(None, None), size=(400, 300),
                background= 'kivy_img/NOT_AVAILABLE background.png')

    pop.open()

def dev_info_pop(device_info, trash):               
    """Popup with device information
        Input:
        device_info - information about device in dictionary form
        trash - pointer to kivy instance
    """
    box = BoxLayout(orientation = 'vertical')
    dev_description = "Name: " + device_info['name'] +"\nMAC: " + device_info['mac']
    
    #Get additional data for not available device
    if device_info['status'] != 'AVAILABLE':
        owner_info = database.get_order_info(device_info['part_id'])
        dev_description += \
            "\nName: " + owner_info['name']+\
            "\nSurname: "+ owner_info['surname']+\
            "\nE-mail: " + owner_info['email']+\
            "\nPhone: " + owner_info['phone']+\
            "\nDate of return: " + str(device_info['return_date'])

        
    #Add label and logo
    box.add_widget(Label(text= dev_description, halign = 'center'))
    logo = Image(source='kivy_img/LOGO.png')
    logo.size_hint = (0.8, 0.8)
    logo.pos_hint = {'x' : 0.1}
    box.add_widget(logo)
    pop = Popup(title = "Device info",
                content=box,
                separator_height = 4,
                title_size = 19,
                size_hint=(None, None), size=(400, 350),
                background= 'kivy_img/NOT_AVAILABLE background.png')

    pop.open()

def scan_student_card():
    """Popup - scan your student card information
        Reurns pointer to popup
    """
    box = BoxLayout()
    box.add_widget(Label(text='Scan your student card', halign = 'center'))
    pop = Popup(title='Scanning....',
                content=box,
                separator_height = 4,
                title_size = 19,
                size_hint=(None, None), size=(300, 200),
                auto_dismiss = False,                           #can't be closed
                background= 'kivy_img/NOT_AVAILABLE background.png')

    pop.open()
    return pop

def nfc_detection(status):  
        """Changing screen
            If device is not available we go to return screen
            If available to renting screen
            If device not exist in our base we go to "not exist screen" where we could add newone
        """     
        if status == "NOT_AVAILABLE" :
            sm.current="return_screen"
            sm.transition.direction="up"

        if status == "AVAILABLE" :
            sm.current="renting_screen"
            sm.transition.direction="left"

        if status == "NOT_PRESENT" :
            sm.current="not_exist_screen"
            sm.transition.direction="right"




kv = Builder.load_file("rfid.kv")

sm = ScreenManager()
screens = [Main_window(name="main_screen"), Renting_window(name="renting_screen"),Return_window(name="return_screen"),Not_exist_window(name="not_exist_screen")]
for screen in screens:
    sm.add_widget(screen)

sm.current="main_screen"

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')   #<no red dots on screen


    
