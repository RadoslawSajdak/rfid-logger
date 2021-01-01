from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import date, datetime
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import testy
import Database as database
from kivy.config import Config
from functools import partial ##import partial, wich allows to apply arguments to functions returning a funtion with that arguments by default.

class Personal_label(FloatLayout):
    """Work in progres - test functionality"""
    pass

class Main_window(Screen):
    """Main window design and functionality"""
    info = ObjectProperty(None)
    
    def dev_base(self):
        """Print out list of defices in our database"""
        top_button_share = 1.1
        self.ids.list.clear_widgets()

        for i in range (len(self.dev_data)):
            top_button_share -= .4

            if self.dev_data[i]["status"]=="AVAILABLE":
                button_share = \
                    Button(pos_hint={"x": 0, "top": top_button_share},
                            size_hint_y=None, 
                            height=40,
                            text = str(self.dev_data[i]["name"])+"   "+str(self.dev_data[i]["status"]))
                          
            else:
                button_share = \
                    Button(pos_hint={"x": 0, "top": top_button_share},
                            size_hint_y=None, 
                            height=40,
                            text = str(self.dev_data[i]["name"])+"   "+str(self.dev_data[i]["return_date"]))
            device = "Name: %s \nMAC: %s \n + Whatever you want" % (self.dev_data[i]['name'], self.dev_data[i]['mac'])
            button_callback = partial(dev_info, device)        #Send argument to function
            button_share.bind(on_press = button_callback)  

            self.ids.list.add_widget(button_share)

    def on_enter(self):
        """Update local values"""
        self.dev_data = database.get_devices()   ###FROM DATABASE: list of devices
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

    def on_enter(self):
        """Get data from database and update internal variables """
        user, part = database.get_order(database.MAC_db)  ##TODO change this function to get_device
        self.dev_data = part   

        self.dev_name.text = self.dev_data["name"]
        self.dev_id.text = str(self.dev_data["part_id"])
        self.dev_mac.text = self.dev_data["mac"]

        pass
    
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
            self.renting_user={"name":self.us_name.text, "surname": self.us_surname.text, "index": self.us_index.text, \
                "email" : self.us_phone.text, "return_date" : self.return_date.text}
            ##TODO write self.renting_user into database  --- format line above
            sm.current= "main_screen"
            sm.transition.direction = "right"

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
        datestr = datetime.now()
        try:
            datestr = datetime.strptime(self.return_date.text, '%Y-%m-%d')
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
            #self.returndate.text               #TODO (NEW RETURN DATE) BREAKPOINT    prologue
            sm.transition.direction = "down"
            sm.current = "main_screen"
        else:
            #Devive returned
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
        if len(value)<2:
            required_info(value_type)
        return 0 if len(value)<2 else 1

    def add_button(self):
        """Add button functionality"""
        self.correct = self.empty_value("Device name", self.dev_name.text)
        if(self.correct):
            self.new_name={"name":self.dev_name.text}
            ##TODO take this name 
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
    pop = Popup(title='Invalid Form',
                  content=Label(text='Data format incorrect\nPlease use YYYY-MM-DD format'),
                  size_hint=(None, None), size=(400, 200))

    pop.open()

def required_info(info_name):
    """Popup to tell that information written by user is not correct"""
    pop = Popup(title = "Required info",
                content=Label(text='This information is required :' + info_name),
                size_hint=(None, None), size=(400, 200))

    pop.open()

def dev_info(arg, trash):
    """Popup with device information"""
    pop = Popup(title = "Device info",
                content=Label(text='Device information:\n' + arg),
                size_hint=(None, None), size=(400, 200))

    pop.open()


kv = Builder.load_file("rfid.kv")

sm = ScreenManager()
screens = [Main_window(name="main_screen"), Renting_window(name="renting_screen"),Return_window(name="return_screen"),Not_exist_window(name="not_exist_screen")]
for screen in screens:
    sm.add_widget(screen)

sm.current="main_screen"

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')   #<no red dots on screen

class Rfid_App(App):
    """Main aplication class - must have"""
    def build(self):
        return sm
    
