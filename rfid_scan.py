from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import date
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout


class MainWindow(Screen):
    
    def base(self):
        top_button_share = 1.1

        self.ids.list.clear_widgets()

        def build(self):
            # Create the screen manager
            sm = ScreenManager()
            sm.add_widget(MenuScreen(name='main'))
            sm.add_widget(SettingsScreen(name='return'))

            return sm

        for i in range(50):
            top_button_share -= .4

            button_share = \
                Button(pos_hint={"x": 0, "top": top_button_share},
                        size_hint_y=None, 
                        height=40,
                        text = str(i))

            self.ids.list.add_widget(button_share)
        

    def __init__(self, **kwargs):
        super(MainWindow,self).__init__(**kwargs)
        
        pass 

    pass

class RentingWindow(Screen):
    def fun(self):
        print("Hello")
        funkcja()
        tekst = "test"
        return tekst

    def today(self):
        today = date.today()
        return today.strftime("%d-%B-%Y")



class ReturnWindow(Screen):
    def today(self):
        today = date.today()
        return today.strftime("%d-%B-%Y")


class NotExistWindow(Screen):
    pass

class MenagerWindow(ScreenManager):
    main_window = ObjectProperty(None)
    return_window = ObjectProperty(None)



kv = Builder.load_file("rfid.kv")

class RFIDApp(App):
    def build(self):
        return kv

def funkcja():
    print("World")

arrr = ["a", "b", "c"]
for i in arrr:
    print(i)

if __name__ == "__main__" :
    RFIDApp().run()
    