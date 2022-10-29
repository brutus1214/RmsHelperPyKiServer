import socket
import pyodbc
import logging

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.config import Config
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol

# class to build GUI for a popup window
class P(FloatLayout):
    pass

class RMSHelperTCP(protocol.Protocol):
    def dataReceived(self, data):
        logging.info('Received Message')
        response = self.factory.app.handle_message(data)
        if response:
            logging.info('Response Message')
            self.transport.write(response)

class RMSHelperTCPFactory(protocol.Factory):
    protocol = RMSHelperTCP

    def __init__(self, app):
        self.app = app

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')
    btn_info = ListProperty(['Button 0 Text', 'Button 1 Text', 'Button 2 Text', 'Button 3 Text', 'Button 4 Text', 'Button 5 Text'])

class ConnectionList(RecycleView):
    rv_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ConnectionList, self).__init__(**kwargs)
        self.data = [{'text': "Button " + str(x), 'id': str(x)} for x in range(6)]

class loginWindow(Screen):
    pass

class serverWindow(Screen):
    pass

# class for managing screens
class windowManager(ScreenManager):
    pass

sm = windowManager()


class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        # kv file
        kv = Builder.load_file('windows.kv')

        # TODO: Had to start on build, why not during App
        reactor.listenTCP(8000, RMSHelperTCPFactory(self))
        # adding screens
        sm.add_widget(loginWindow(name='login'))
        sm.add_widget(serverWindow(name='server'))
        sm.current = 'server'
        return sm

    def disp_msg(self, name):
        menuscreen = self.root.get_screen('login')
        menuscreen.ids.msg_label.text = f'Sup {name}!'

    def read(self, conn):
        cursor = conn.cursor()
        cursor.execute("select * from Item where ItemLookupCode = '735'")
        #print(cursor)

    # function that displays the content
    def popFun(self):
        show = P()
        window = Popup(title="Please enter valid information?", content=show,
                       size_hint=(None, None), size=(300, 100))
        window.open()

    def rmshelper_server_connect(self):
        self.disp_msg("PyCharm Start")
        menuscreen = self.root.get_screen('login')
        if len(menuscreen.ids.server.text) and len(menuscreen.ids.dbname.text) and len(menuscreen.ids.password.text) != 0:
            try:
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 18 for SQL Server};'
                    'SERVER=' + menuscreen.ids.server.text + ',1433;'
                    'DATABASE=' + menuscreen.ids.dbname.text + ';'
                    'UID=sa;'
                    'PWD=' + menuscreen.ids.password.text + ';'
                    'TrustServerCertificate=yes;'
                )
                #self.read(conn)
                sm.current = 'server'


            except pyodbc.Error as err:
                self.popFun()
                self.clear()
        else:
            self.popFun()

        self.disp_msg("PyCharm End")

        #read(conn)
        #self.root.ids.rmshelper_label.text = f'Sup {self.root.ids.server.text}!'


    def clear(self):
        menuscreen = self.root.get_screen('login')
        menuscreen.ids.rmshelper_label.text = "RMSHelper Server"
        menuscreen.ids.server.text = ""
        menuscreen.ids.dbname.text = ""
        menuscreen.ids.password.text = ""

    def exit(self):
        return self.root_window.close()

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.disp_msg(msg)

        if msg == "ping":
            msg = "Pong"
        if msg == "plop":
            msg = "Kivy Rocks!!!"
        self.disp_msg(msg)
        return msg.encode('utf-8')

# driver function
if __name__ == "__main__":
    MainApp().run()