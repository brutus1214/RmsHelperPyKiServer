import socket
import pyodbc

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp


# class to build GUI for a popup window
class P(FloatLayout):
    pass


class connectionWindow(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('connection.kv')


class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('login.kv')

    def disp_msg(self, name):
        self.root.ids.msg_label.text = f'Sup {name}!'

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

        if len(self.root.ids.server.text) and len(self.root.ids.dbname.text) and len(self.root.ids.password.text) != 0:
            try:
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 18 for SQL Server};'
                    'SERVER=' + self.root.ids.server.text + ',1433;'
                    'DATABASE=' + self.root.ids.dbname.text + ';'
                    'UID=sa;'
                    'PWD=' + self.root.ids.password.text + ';'
                    'TrustServerCertificate=yes;'
                )
                #self.read(conn)
                #connectionWindow().run()

            except pyodbc.Error as err:
                self.popFun()
                self.clear()
        else:
            self.popFun()

        self.disp_msg("PyCharm End")

        #read(conn)
        #self.root.ids.rmshelper_label.text = f'Sup {self.root.ids.server.text}!'


    def clear(self):
        self.root.ids.rmshelper_label.text = "RMSHelper Server"
        self.root.ids.server.text = ""
        self.root.ids.dbname.text = ""
        self.root.ids.password.text = ""


MainApp().run()