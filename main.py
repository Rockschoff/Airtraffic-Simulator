# main.py
# Description: 
#   Contains the definition of the application

import time
from kivy.app import App
from kivy.lang import Builder
import Screens
import MasterLogAccess
import TestingDatabases

main = Builder.load_file("main.kv")
#test = TestingDatabases.TestingDatabases()
    
class Air_Traffic_Control_System(App):
    def build(self):
        return main

if __name__ == '__main__':
    Air_Traffic_Control_System().run()
