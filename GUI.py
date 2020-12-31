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

class MainWindow(Screen):
    
    def dev_base(self):
        top_button_share = 1.1
        print(self)
        self.ids.list.clear_widgets()

        for i in range (len(self.dev_data)):
            top_button_share -= .4

            if self.dev_data[i]["status"]=="available":
                button_share = \
                    Button(pos_hint={"x": 0, "top": top_button_share},
                            size_hint_y=None, 
                            height=40,
                            text = str(self.dev_data[i]["name"])+str(self.dev_data[i]["status"]))
                          
            else:
                button_share = \
                    Button(pos_hint={"x": 0, "top": top_button_share},
                            size_hint_y=None, 
                            height=40,
                            text = str(self.dev_data[i]["name"])+str(self.dev_data[i]["return_date"]))

            button_share.bind(on_press = funkcja)  

            self.ids.list.add_widget(button_share)

    def on_enter(self):
        self.dev_data = testy.get_parts()   ###<-list of dev + year here I NEED
        
        pass
        

    def __init__(self, **kwargs):
        super(MainWindow,self).__init__(**kwargs)
        pass 

    def NFC_detection(status):                           ##<< CHANGING SCREEN
        sm.current="return" if status == "NotReturned" else "renting"
        sm.transition.direction="up" if status == "NotReturned" else "left"

class RentingWindow(Screen):

    def on_enter(self):
        pass
    

    def today(self):
        today = date.today()
        return today.strftime("%d-%B-%Y")



class ReturnWindow(Screen):

    def on_enter(self):
        self.user_data = testy.user_data()      ##<<<<HERE I NEED USER DATA
        self.dev_data = testy.get_part()       ##<<<<HERE I NEED DEVICE DATA
        
        self.us_name.text = self.user_data["name"]
        self.us_surname.text = self.user_data["surname"]
        self.us_index.text = self.user_data["student_id"]
        self.us_email.text = self.user_data["email"]
        self.us_phone.text = self.user_data["phone"]
        self.us_project.text = self.user_data["project"]

        self.dev_name.text = self.dev_data["name"]
        self.dev_id.text = str(self.dev_data["part_id"])
        self.dev_mac.text = self.dev_data["mac"]
        pass

    def today(self):
        today = date.today()
        print(today)
        return today.strftime("%d-%B-%Y")

    def checkDate(self):
        datestr = datetime.now()
        try:
            datestr = datetime.strptime(self.returndate.text, '%Y-%m-%d')
        except:
            pass
        today = datetime.now()
        if(datestr > today):  #OK
            self.returnButtonID.text = "Prologue"
        else:
            self.returnButtonID.text = "Return"
            invalidTime()

    def returnButton(self):
        if self.returnButtonID.text == "Prologue":
            #Device prologue
            #self.returndate.text               #(NEW RETURN DATE) BREAKPOINT    
            sm.transition.direction = "down"
            sm.current = "main"
        else:
            #Devive returned
            pass


    def cancelButton(self):
        self.returndate.text = " "
        sm.transition.direction = "down"
        sm.current = "main"

class NotExistWindow(Screen):
    pass



def invalidTime():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Data format incorrect\nPlease use YYYY-MM-DD format'),
                  size_hint=(None, None), size=(400, 200))

    pop.open()

def requiredInfo(infoName):
    pop = Popup(title = "Required info",
                content=Label(text='This information is required:' + infoName),
                size_hint=(None, None), size=(400, 200))

    pop.open()


kv = Builder.load_file("rfid.kv")

sm = ScreenManager()
screens = [MainWindow(name="main"), RentingWindow(name="renting"),ReturnWindow(name="return"),NotExistWindow(name="notexist")]
for screen in screens:
    sm.add_widget(screen)

sm.current="return"

class RFIDApp(App):
    def build(self):
        return sm

def funkcja(arg):
    print(arg)
    print("World")


if __name__ == "__main__" :
    data = testy.user_data()
    for i in data:
        print(i)
    print(data["name"])

    RFIDApp().run()
    