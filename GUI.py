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


class Main_window(Screen):
    """Main window design and functionality"""
    info = ObjectProperty(None)
    
    def dev_base(self):
        """Print out list of defices in our database"""
        top_button_share = 1.1
        self.ids.list.clear_widgets()

        for i in range (len(self.dev_data)):
            top_button_share -= .1
            button_share = Button(pos_hint={"x": 0, "top": top_button_share},
                            size_hint_y=None, 
                            height=40)
            spaces = 70*" "
            dev_information = str(self.dev_data[i]["name"])
            if self.dev_data[i]["status"]=="AVAILABLE":
                dev_information += spaces[len(str(self.dev_data[i]["name"])): -len(str(self.dev_data[i]["status"]))]      
                dev_information += str(self.dev_data[i]["status"])     
                button_share.background_color = get_color_from_hex('#6FAF8B') 
                button_share.background_normal = ""      
                button_share.color = (0, 0, 0, 1)                            
            else:
                dev_information += spaces[len(str(self.dev_data[i]["name"])): -len(str(self.dev_data[i]["return_date"]))]    
                dev_information += "    "
                dev_information += str(self.dev_data[i]["return_date"]) 
                today = date.today()
                button_share.background_normal = ""      
                button_share.color = (0, 0, 0, 1)  
                if today >= self.dev_data[i]["return_date"]:
                    button_share.background_color = get_color_from_hex('#FF5733') 
                else:
                    button_share.background_color = get_color_from_hex('#a6a6a6')
                        

            button_share.text = dev_information

            device = "Name: %s \nMAC: %s \n + Whatever you want" % (self.dev_data[i]['name'], self.dev_data[i]['mac'])
            button_callback = partial(dev_info, device)        #Send argument to function
            button_share.bind(on_press = button_callback)  

            self.ids.list.add_widget(button_share)

    def on_enter(self):
        """Update local values"""
        self.dev_data = database.get_all_devices()   ###FROM DATABASE: list of devices
        pass
        

    def __init__(self, **kwargs):
        """Not necessery now"""
        super(Main_window,self).__init__(**kwargs)
        pass 

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


class Renting_window(Screen):
    """Renting window design and functionality"""

    us_data = {                            #data buffor
            "user_id" : "",
            "name" : "",
            "surname" : "",
            "student_id" : "",
            "email" : "",
            "phone" : ""}

    def on_enter(self):
        """Get data from database and update internal variables """
        db_data = database.get_one_part(database.MAC_db)
        self.dev_data = db_data   

        

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
            datestr = datetime.strptime(self.return_date.text, '%d-%m-%Y')
        except:
            pass
        today = datetime.now()
        if not(datestr > today):
            invalid_time()
        return 0 if not(datestr > today) else 1

    def today(self):
        """Get actual date"""
        today = date.today()
        return today.strftime("%d-%B-%Y")

    def empty_value(self, value_type, value):
        """Check if value is empty - some data are required
            return if(not empty)
        """
        if len(value)<2:
            required_info(value_type)
        return 0 if len(value)<2 else 1
    
    def rent_button(self):
        """Rent button functionality
            Check required values - if(not empty) - name, surname, email
            Next window and write data into base
        """
        self.correct = self.empty_value("Name",self.us_name.text)
        if (self.correct) :
            self.correct = self.empty_value("Surname",self.us_surname.text) 
        if (self.correct) :
            self.correct = self.empty_value("E-mail",self.us_email.text)
        if (self.correct) :
            self.correct = self.check_date() 
        if (self.correct) :
            self.renting_user={"name":self.us_name.text, "surname": self.us_surname.text, "student_id": self.us_index.text, \
                "email" : self.us_email.text, "phone" : self.us_phone.text, "return_date" : self.return_date.text}
            database.rent_item(database.MAC_db, self.renting_user)
            sm.current= "main_screen"
            sm.transition.direction = "right"

    def scan_student_card_button(self):
        ##TODO your function - scaning ID
        self.us_data["name"] = "Radosław"
        #self.us_data =      #<<TODO information from base 
        self.on_enter()
        pass

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
        print(user)
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
        print(self.user_data)
        pass

    def today(self):
        """Get actual date"""
        today = date.today()
        print(today)
        return today.strftime("%d-%B-%Y")

    def check_date(self):
        """Check if written data is correct (format/value bigger than today's date)
            returning if(correct)
        """
        datestr = self.today()
        try:
            datestr = datetime.strptime(self.return_date.text, '%d-%m-%Y')
        except:
            pass
        today = datetime.now()
        if(datestr > today):
            self.return_button_id.text = "Prologue"
        else:
            self.return_button_id.text = "Return"
            invalid_time()

    def return_button(self):
        """Return button procedure
            Prologue or return
        """
        if self.return_button_id.text == "Prologue":
            #Device prologue
            #database.prologue(self.dev_data["part_id"], self.return_date )             #TODO (NEW RETURN DATE) BREAKPOINT    prologue
            sm.transition.direction = "down"
            sm.current = "main_screen"
        else:
            #Devive returned
            database.return_item(self.dev_data["mac"])
            sm.transition.direction = "down"
            sm.current = "main_screen"
            pass


    def cancel_button(self):
        """Cancel button functionality
            return to main window
        """
        self.return_date.text = " "
        sm.transition.direction = "down"
        sm.current = "main_screen"

class Not_exist_window(Screen):
    """Not exist window design and functionality"""
    def on_enter(self):
        """Get data from database and update internal variables """
        self.dev_mac.text=database.MAC_db
        pass

    def empty_value(self, value_type, value):
        """Check if value is empty - some data are required
            return if(not empty)
        """
        if (len(value)<2 or len(value)>40) :
            required_info(value_type+ "  must be 2-40 character long")
        return 0 if (len(value)<2 or len(value)>40) else 1

    def add_button(self):
        """Add button functionality"""
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




def invalid_time():
    """Popup to tell that data is not correct"""
    box = BoxLayout()
    box.add_widget(Label(text='Please use DD-MM-YYYY format', halign = 'center'))
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

def dev_info(arg, trash):
    """Popup with device information"""
    box = BoxLayout()
    box.add_widget(Label(text= arg, halign = 'center'))
    pop = Popup(title = "Device info",
                content=box,
                separator_height = 4,
                title_size = 19,
                size_hint=(None, None), size=(500, 400),
                background= 'kivy_img/NOT_AVAILABLE background.png')

    pop.open()


kv = Builder.load_file("rfid.kv")

sm = ScreenManager()
screens = [Main_window(name="main_screen"), Renting_window(name="renting_screen"),Return_window(name="return_screen"),Not_exist_window(name="not_exist_screen")]
for screen in screens:
    sm.add_widget(screen)

sm.current="return_screen"

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')   #<no red dots on screen

class Rfid_App(App):
    """Main aplication class - must have"""
    def build(self):
        return sm
    
