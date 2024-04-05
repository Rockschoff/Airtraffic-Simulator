# Screens.py
# Description:
#   Contains the definitions for classes for the associated widgets in every screen
#   This file will be split into files for each screen in the future

# When trying to login use "Admin1" for username and "Test1234" for the password

from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
import time
from kivy.graphics import *
from kivy.graphics import Color
import threading
from kivy.uix import *
from datetime import datetime, timedelta
import math
import MasterLogAccess
import IncidentLogAccess
from random import randint

# Set window size
Window.size = (1280, 720)
Window.minimum_width, Window.minimum_height = Window.size

# Planes to use in th
examplePlanes = [{
    "id": "000001",
    "airline": "American Airlines",
    "gasUsage": (str(randint(90, 110)/100)), # in gal/s
    "altitude": str(randint(39950, 40050)), # in mi
    "expectedAltitude": 40000, # in mi
    "weight": 180678, # in lbs
    "weightCapacity": 205000, # in lbs
    "runway": "Runway 1",
    "dockingGate": "Gate 1",
    "expectedRateOfDescent": 2000, # in ft/min
    "airliner": "Airbus A321-200",
    "flightStatus": "Departing"
}, 
{
    "id": "000002",
    "airline": "Delta Airlines",
    "gasUsage": (str(randint(90, 110)/100)), # in gal/s
    "altitude": str(randint(39950, 40050)), # in mi
    "expectedAltitude": 40000, # in mi
    "weight": 130105, # in lbs
    "weightCapacity": 157300, # in lbs
    "runway": "Runway 1",
    "dockingGate": "Gate 1",
    "expectedRateOfDescent": 2000, # in ft/min
    "airliner": "Boeing 737",
    "flightStatus": "Preparing"
}, 
{
    "id": "000003",
    "airline": "United Airlines",
    "gasUsage": (str(randint(90, 110)/100)), # in gal/s
    "altitude": str(randint(39950, 40050)), # in mi
    "expectedAltitude": 40000, # in mi
    "weight": 101582, # in lbs
    "weightCapacity": 133004, # in lbs
    "runway": "Runway 1",
    "dockingGate": "Gate 1",
    "expectedRateOfDescent": 2000, # in ft/min
    "airliner": "Boeing 737-700",
    "flightStatus": "Preparing"
    
},
{
    "id": "000004",
    "airline": "American Airlines",
    "gasUsage": (str(randint(90, 110)/100)), # in gal/s
    "altitude": str(randint(39950, 40050)), # in mi
    "expectedAltitude": 40000, # in mi
    "weight": 185188, # in lbs
    "weightCapacity": 205000, # in lbs
    "runway": "Runway 1",
    "dockingGate": "Gate 1",
    "expectedRateOfDescent": 2000, # in ft/min
    "airliner": "Airbus A321-200",
    "flightStatus": "In Flight"
}
]

# 888888 888888 8b    d8 88""Yb 88        db    888888 888888 .dP"Y8 
#   88   88__   88b  d88 88__dP 88       dPYb     88   88__   `Ybo." 
#   88   88""   88YbdP88 88"""  88  .o  dP__Yb    88   88""   o.`Y8b 
#   88   888888 88 YY 88 88     88ood8 dP""""Yb   88   888888 8bodP' 

class TitleLabel(Label):
    pass

class TopBarLayout(GridLayout):
    title_text = StringProperty()
    def __init__(self, **kwargs):
        super(TopBarLayout, self).__init__(**kwargs)

# this variable is so that animation does not start until a certain screen in
startMoving = False

# Class for WindowManager controller - needed to change screens
class WindowManager(ScreenManager):
    login = ObjectProperty(None)
    mainMenu = ObjectProperty(None)
    radar = ObjectProperty(None)

# 88""Yb    db    8888b.     db    88""Yb 
# 88__dP   dPYb    8I  Yb   dPYb   88__dP 
# 88"Yb   dP__Yb   8I  dY  dP__Yb  88"Yb  
# 88  Yb dP""""Yb 8888Y"  dP""""Yb 88  Yb 

#this is the code for the radar page
class RadarWindow(Screen):

    #these are the variable that corresponds with planes
    global startMoving
    plane1 = ObjectProperty(None)
    plane2 = ObjectProperty(None)
    plane3 = ObjectProperty(None)
    plane4 = ObjectProperty(None)
    label1 = ObjectProperty(None)
    label2 = ObjectProperty(None)
    label3 = ObjectProperty(None)
    label4 = ObjectProperty(None)
    planeInfo = ObjectProperty(None)
    filler = ObjectProperty(None)
    separator = ObjectProperty(None)

    #use to move the plane in order
    plane1On = True
    plane2On = False
    plane3On = False
    plane4On = False
    
    #use to pop up plane info when arrive
    infoOn = True
    infoOn2 = True
    newLabel = Label
    newFiller = Widget
    newSeparator = Label

    # Bad weather
    badWeather = False

    #use to update status text
    statusText1 = "Good"
    statusText2 = "Good"
    statusText3 = "Good"
    statusText4 = "Good"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #update screen every .1 seconds
        Clock.schedule_interval(self.update, .25)

    def makeGoodWeather(self, dt):
        self.badWeather = False
        
    #the method for the animation
    def update(self, dt):
        #disable label until plane is in sight
        if(self.infoOn2):
            self.infoOn2 = False
            self.newLabel = self.label4
            self.newSeparator = self.separator
            self.planeInfo.remove_widget(self.label4)
            self.planeInfo.remove_widget(self.separator)

        #calculating height and width range
        h1 = self.height - dp(20)
        w1 = self.width * 2/3 - dp(20)

        #get current plan posistion
        x1, y1 = self.plane1.pos
 
        x2, y2 = self.plane2.pos
        
        x3, y3 = self.plane3.pos
   
        x4, y4 = self.plane4.pos
        
        #displaying plane infor
        self.label1.text = "ID               : 000001\nPosition     : " + str(int(x1)) + ", " + str(int(y1)) + " \nAirline        : American Airlines\nStatus        : " + self.statusText1 
        self.label2.text = "ID               : 000002\nPosition     : " + str(int(x2)) + ", " + str(int(y2)) + " \nAirline        : Delta Airlines\nStatus        : " + self.statusText2
        self.label3.text = "ID               : 000003\nPosition     : " + str(int(x3)) + ", " + str(int(y3)) + " \nAirline        : United Airlines\nStatus        : " + self.statusText3
        self.label4.text = "ID               : 000004\nPosition     : " + str(int(x4)) + ", " + str(int(y4)) + " \nAirline        : American Airlines\nStatus        : " + self.statusText4

        #pause movement until the radar screen is shown
        if(startMoving):
            #updating plan position
            #this is for demonstation purposes
            #if we had access to actual plane movement this is where it will go
            #changing status depending on condition
            if(self.plane1On):
                self.statusText1 = "Good, Departing"
                self.plane1.pos = (x1 + dp(5), y1 + dp(5))

                for p in examplePlanes:
                    if int(p["id"]) == 1:
                        p["flightStatus"] = "Departing"

            if(self.plane2On):
                self.statusText2 = "Good, Departing"
                self.plane2.pos = (x2 - dp(5), y2 + dp(3))

                for p in examplePlanes:
                    if int(p["id"]) == 2:
                        p["flightStatus"] = "Departing"
            
            if(self.plane3On):
                self.statusText3 = "Good, Departing"
                self.plane3.pos = (x3, y3 + dp(5))

                for p in examplePlanes:
                    if int(p["id"]) == 3:
                        p["flightStatus"] = "Departing"

            if(self.plane4On):
                if(x4 < dp(400)):
                    self.statusText4 = "Good, Landing"
                    self.plane4.pos = (x4 + dp(5), y4)

                for p in examplePlanes:
                    if int(p["id"]) == 4:
                        p["flightStatus"] = "Landing"
                
            if(x4 >= 400):
                self.statusText4 = "Good, Landed"
                self.label4.text = "ID               : 000004\nPosition     : " + str(int(x4)) + ", " + str(int(y4)) + " \nAirline        : American Airlines\nStatus        : " + self.statusText4
                
                for p in examplePlanes:
                    if int(p["id"]) == 4:
                        p["flightStatus"] = "Landed"

            #only add widget once
            if(x4 + dp(20) > 0 and self.infoOn):
                self.infoOn = False
                self.newFiller = self.filler
                self.planeInfo.remove_widget(self.filler)
                self.planeInfo.add_widget(self.newLabel)
                self.planeInfo.add_widget(self.newSeparator)
                self.planeInfo.add_widget(self.newFiller)

            #removing plane if it is out of bound of  radar
            if(x1 > w1 or x1 < 0 or y1 > h1 or y1 < 0):
                self.plane1On = False
                self.planeInfo.remove_widget(self.label1)
                self.remove_widget(self.plane1)
                if self.badWeather == False:
                    self.plane2On = True

            if(x2 > w1 or x2 < 0 or y2 > h1 or y2 < 0):
                self.plane2On = False
                self.planeInfo.remove_widget(self.label2)
                self.remove_widget(self.plane2)
                if self.badWeather == False:
                    self.plane3On = True
                    self.plane4On = True

            if(x3 > w1 or x3 < 0 or y3 > h1 or y3 < 0):
                self.plane3On = False
                self.planeInfo.remove_widget(self.label3)
                self.remove_widget(self.plane3)

            if(x4 > w1 or y4 > h1 or y4 < 0):
                self.plane4On = False
                self.planeInfo.remove_widget(self.label4)
                self.remove_widget(self.plane4)

    def createWeatherIncident(self):
        Clock.schedule_once(self.makeGoodWeather, 30)
        self.badWeather = True
        incident_log_access.add_Row(23, "Bad weather detected")

#class for plane
class Plane(Widget):
    pass

# 88      dP"Yb   dP""b8 88 88b 88 
# 88     dP   Yb dP   `" 88 88Yb88 
# 88  .o Yb   dP Yb  "88 88 88 Y88 
# 88ood8  YbodP   YboodP 88 88  Y8 

# Class for LoginWindow root widget
class LoginWindow(Screen):
    #ObjectPropert retrieve the text input from the .kv file
    userSubmit = ObjectProperty(None)
    passwordSubmit = ObjectProperty(None)
    #textSubmit is use to display successful login or a message saying wrong username and/or password
    textSubmit = StringProperty("")

    # account is a list of tuple that has username as key and password as value
    # Dillon have the list of valid user here
    account = [("Admin1", "Test1234"),
               ("Admin2", "Password")]
               
    def __init__(self, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        global master_log_access
        global incident_log_access
        global data
        master_log_access = MasterLogAccess.MasterLogAccess()
        incident_log_access = IncidentLogAccess.IncidentLogAccess()
        with self.canvas:
            Color(0.3922, 0.4314, 0.4078, 1)

    #This function is called when the submit button is hit
    def onSubmit(self):

        valid = False

        #this for loop checks if the username and password are in the account list
        for i, tuple in enumerate(self.account):
            if (tuple[0] == self.userSubmit.text and tuple[1] == self.passwordSubmit.text):
                valid = True

        #if it is, set textSubmit to success and change to the main menu
        if valid:
            self.manager.current = "menuScreen"
            self.textSubmit = ""
            self.ids.User.text = ""
            self.ids.Password.text = ""
        #else display incorrect username or password message
        else:
            self.textSubmit = "Incorrect username or password."

# 8b    d8    db    88 88b 88     8b    d8 888888 88b 88 88   88 
# 88b  d88   dPYb   88 88Yb88     88b  d88 88__   88Yb88 88   88 
# 88YbdP88  dP__Yb  88 88 Y88     88YbdP88 88""   88 Y88 Y8   8P 
# 88 YY 88 dP""""Yb 88 88  Y8     88 YY 88 888888 88  Y8 `YbodP' 

# Class for MainMenuWindow root widget
class MainMenuWindow(Screen):
    def changeToRadar(self):
        global startMoving
        startMoving = True
        self.manager.current = "radarScreen"
        self.manager.transition = SlideTransition(direction='right', duration=.25)

# 88""Yb 88        db    88b 88 888888     88 88b 88 888888  dP"Yb      Yb        dP 88 88b 88 8888b.   dP"Yb  Yb        dP 
# 88__dP 88       dPYb   88Yb88 88__       88 88Yb88 88__   dP   Yb      Yb  db  dP  88 88Yb88  8I  Yb dP   Yb  Yb  db  dP  
# 88"""  88  .o  dP__Yb  88 Y88 88""       88 88 Y88 88""   Yb   dP       YbdPYbdP   88 88 Y88  8I  dY Yb   dP   YbdPYbdP   
# 88     88ood8 dP""""Yb 88  Y8 888888     88 88  Y8 88      YbodP         YP  YP    88 88  Y8 8888Y"   YbodP     YP  YP    

# Class for PlaneInfoWindow root widget
class PlaneInfoWindow(Screen):

    def search(self):
        # Getting the text values from text inputs
        searchKey = self.ids.PlaneInfoTextInput.text

        # make a new dataset based on search terms
        newData = []
        for x in getattr(self.ids.PlaneInfoList, 'data'):
            # Ensure that row matches search criteria
            if searchKey == "" or (searchKey.lower() in str(x[0]).lower()):
                newData.append({'dataName': str(x[0]),
                                'dataValue': str(x[1])})
        self.ids.PlaneInfoList.rv.data = newData

    def getInfo(self):
        planeInfoIDText = self.ids.PlaneInfoPlaneID.text

        # Check for an invalid id
        try: 
            planeInfoID = int(planeInfoIDText)
        except: 
            self.ids.PlaneInfoPlaneIDGetInfoResult.text = "Invalid plane ID"
            return

        # Check for an invalid id
        if planeInfoID < 0:
            self.ids.PlaneInfoPlaneIDGetInfoResult.text = "Invalid plane ID"
            return

        # Reset result text if plane id is valid
        self.ids.PlaneInfoPlaneIDGetInfoResult.text = ''
        
        # Search for a plane of the given id, populate list if found
        for p in examplePlanes:
            if int(p["id"]) == planeInfoID:
                self.ids.PlaneInfoList.populate(p)
                return
        
        # No plane found with the given id
        self.ids.PlaneInfoPlaneIDGetInfoResult.text = "No plane found with ID: " + planeInfoIDText



# Class for a row in the table of plane information in PlaneInfo Screen
class PlaneInfoRow(RecycleDataViewBehavior,BoxLayout):
    dataName = StringProperty()
    dataValue = StringProperty()
    def __init__(self, **kwargs):
        super(PlaneInfoRow, self).__init__(**kwargs)

# Class for the list of plane information in PlaneInfo Screen
#   Autopopulates on the first clock
class PlaneInfoList(BoxLayout):
    currentPlaneInfoID = -1
    def __init__(self, **kwargs):
        super(PlaneInfoList, self).__init__(**kwargs)
        #Clock.schedule_once(self.finish_init,0) # do not populate at start

    # Autopopulate list of plane info
    def finish_init(self, dt):
        self.populate()

    # Populate list of plane info from database
    def populate(self, plane):
        # query_result = master_log_access.temporary_Info_List_Search()
        
        self.currentPlaneInfoID = int(plane['id'])

        # Given data
        query_result = [
            ['Plane ID', str(plane['id'])],
            ['Airline', str(plane['airline'])],
            ['Flight Status', str(plane['flightStatus'])],
            ['Gas Usage', str(plane['gasUsage']) + " gal/s"],
            ['Altitude', str(plane['altitude']) + " mi"],
            ['Expected Altitude', str(plane['expectedAltitude']) + " mi"],
            ['Weight', str(plane['weight']) + " lbs"],
            ['Weight Capacity', str(plane['weightCapacity']) + " lbs"],
            ['Runway', str(plane['runway'])],
            ['Docking Gate', str(plane['dockingGate'])],
            ['Expected rate of descent', str(plane['expectedRateOfDescent']) + " ft/min"],
            ['Airliner', str(plane['airliner'])]
        ]

        # Populate list with data values
        self.data = query_result
        self.rv.data = [{'dataName': str(x[0]),
        'dataValue': str(x[1])} for x in query_result]

    def refresh(self):
        # Check if id is not currently set
        if self.currentPlaneInfoID < 0:
            return

        # Find plane with current id
        for p in examplePlanes:
            if int(p["id"]) == self.currentPlaneInfoID:
                self.populate(p)
                return

    def makeOverweight(self):
        # Check if id is not currently set
        if self.currentPlaneInfoID < 0:
            return

        # Find plane with current id
        for p in examplePlanes:
            if int(p["id"]) == self.currentPlaneInfoID:
                p["weight"] = p["weightCapacity"] + randint(100, 500)
        
        self.refresh()

# .dP"Y8  dP""b8 88  88 888888 8888b.  88   88 88     888888 
# `Ybo." dP   `" 88  88 88__    8I  Yb 88   88 88     88__   
# o.`Y8b Yb      888888 88""    8I  dY Y8   8P 88  .o 88""   
# 8bodP'  YboodP 88  88 888888 8888Y"  `YbodP' 88ood8 888888 


# Class for ScheduleWindow root widget
class ScheduleWindow(Screen):
    pass

# Class for a row of ArrivalList, the list of arriving planes
class ArrivalRow(RecycleDataViewBehavior,BoxLayout):
    planeName = StringProperty()
    planeArrivalTime = StringProperty()
    def __init__(self, **kwargs):
        super(ArrivalRow, self).__init__(**kwargs)

# Class for a row of DepartureList, the list of departing planes
class DepartureRow(RecycleDataViewBehavior,BoxLayout):
    planeName = StringProperty()
    planeDepartureTime = StringProperty()
    def __init__(self, **kwargs):
        super(DepartureRow, self).__init__(**kwargs)

#https://github.com/kivy/kivy/issues/6582
# Class for the list or arriving planes
class ArrivalList(BoxLayout):
    def __init__(self, **kwargs):
        super(ArrivalList, self).__init__(**kwargs)
        Clock.schedule_once(self.finish_init,0)

    # Autopopulate list of arrivals
    def finish_init(self, dt):
        self.populate()

    # TODO:  Write query for populating list of arrivals
    # Populate list of arrivals
    def populate(self):
        arrivalPlaneNames = ['4']
        dateTimeNow = datetime.now()
        dateTimeA = dateTimeNow.strftime('%a, %b %d, %y  -  %m-%d-%y  -  %H:%M')
        dateTimeNow = datetime.now() + timedelta(hours=6, minutes = 1)
        #dateTimeB = dateTimeNow.strftime('%a, %b %d, %y  -  %m-%d-%y  -  %H:%M')
        #dateTimeNow = datetime.now() + timedelta(hours=2, minutes = 12)
        #dateTimeC = dateTimeNow.strftime('%a, %b %d, %y  -  %m-%d-%y  -  %H:%M')
        arrivalPlaneDatetimes = [dateTimeA]

        self.rv.data = [
            {'planeName': arrivalPlaneNames[x],
             'planeArrivalTime': arrivalPlaneDatetimes[x]}
            for x in range(1)]

# Class for the list of departing planes
class DepartureList(BoxLayout):
    def __init__(self, **kwargs):
        super(DepartureList, self).__init__(**kwargs)
        Clock.schedule_once(self.finish_init,0)

    # Autopopulate list of departures
    def finish_init(self, dt):
        self.populate()

    # TODO: Write query for populating list of departures
    # Populate list of departures
    def populate(self):
        departurePlaneNames = ['1', '2', '3']
        dateTimeNow = datetime.now() + timedelta(hours=3, minutes = 27)
        dateTimeA = dateTimeNow.strftime('%a, %b %d, %y  -  %m-%d-%y  -  %H:%M')
        dateTimeNow = datetime.now() + timedelta(hours=4, minutes = 27)
        dateTimeB = dateTimeNow.strftime('%a, %b %d, %y  -  %m-%d-%y  -  %H:%M')
        dateTimeNow = datetime.now() + timedelta(hours=5, minutes = 12)
        dateTimeC = dateTimeNow.strftime('%a, %b %d, %y  -  %m-%d-%y  -  %H:%M')
        departurePlaneDateteimes = [dateTimeA, dateTimeB, dateTimeC]

        self.rv.data = [
            {'planeName': departurePlaneNames[x],
             'planeDepartureTime': departurePlaneDateteimes[x]}
            for x in range(3)]

# 888888 888888 88""Yb 8b    d8 88 88b 88    db    88         .dP"Y8 88 8b    d8 
#   88   88__   88__dP 88b  d88 88 88Yb88   dPYb   88         `Ybo." 88 88b  d88 
#   88   88""   88"Yb  88YbdP88 88 88 Y88  dP__Yb  88  .o     o.`Y8b 88 88YbdP88 
#   88   888888 88  Yb 88 YY 88 88 88  Y8 dP""""Yb 88ood8     8bodP' 88 88 YY 88 

# Class representing a worker in the simulation of the ground crew simulation
class TerminalSimulatedPlane(Widget):
    def __init__(self, **kwargs):
        super(TerminalSimulatedPlane, self).__init__(**kwargs)

# Class for the TerminalSimulationWindow root widget
class TerminalSimulationWindow(Screen):
    planes = []
    def __init__(self, **kwargs):
        super(TerminalSimulationWindow, self).__init__(**kwargs)
        self.planes = []
        self.initializePlanes()

    # Initialize simulated plane objects
    #   Planes are initialized in an array because adding and referencing them by ids is not possible to do dynamically
    #   Plane number and initial positions are determined by a query (not yet implemented)
    def initializePlanes(self):
        # Figure out the number of planes in the simulation
        # TODO: make a query to determine number of planes
        for x in range(0, 1):
            newPlane = TerminalSimulatedPlane()
            # TODO: Make a query to determine the initial position of each plane
            newPlane.pos = (randint(200,200), randint(200,200))
            self.planes.append(newPlane)
            self.add_widget(self.planes[len(self.planes)-1])

    # Animate the given widget. First rotate to face 
    #   wIndex - String - The index of the widget to animate          
    #   destX - Num - The x position to animate to
    #   destY - Num - The y position to animate to
    #   angleOffset - Num - The offset of the calcuated angle to animate to. 
    #       Default if 0 offset. 
    #       angleOffset should be 45 for GoogleAirplane.png
    def planeAnimate(self, wIndex, destX, destY, angleOffset=0, **kwargs):

        # Check that not already at destination
        if (destX  - self.planes[wIndex].pos[0]) == 0 and (destY - self.planes[wIndex].pos[1]) == 0:
            return

        # Calculate angleOffset
        if (destY - self.planes[wIndex].pos[1]) < 1:
            angleOffset -= 180
        atan = math.atan((destX  - self.planes[wIndex].pos[0]) / (destY - self.planes[wIndex].pos[1]))
        deg = atan * 180 / math.pi
        deg = deg * -1
        addedOffset = deg + angleOffset
        angle = addedOffset

        # Create and start animation
        anim = Animation(animAngle=angle, duration=.2) + Animation(x= destX, y = destY, duration=1)
        anim.start(self.planes[wIndex])

# 8b    d8    db    .dP"Y8 888888 888888 88""Yb     88      dP"Yb   dP""b8 
# 88b  d88   dPYb   `Ybo."   88   88__   88__dP     88     dP   Yb dP   `" 
# 88YbdP88  dP__Yb  o.`Y8b   88   88""   88"Yb      88  .o Yb   dP Yb  "88 
# 88 YY 88 dP""""Yb 8bodP'   88   888888 88  Yb     88ood8  YbodP   YboodP 

class MasterLogWindow(Screen):
    def search(self):
        # Getting the text values from text inputs
        MasterLogDateTimeTextInputText = self.ids.MasterLogDatetimeTextInput.text
        MasterLogPlaneIDTextInputText = self.ids.MasterLogPlaneIDTextInput.text
        MasterLogNoteTextInputText = self.ids.MasterLogNoteTextInput.text

        # make a new dataset based on search terms
        newData = []
        for x in getattr(self.ids.MasterLogList, 'masterLogData'):
            # Ensure that row matches search criteria
            condition = True
            condition = condition and MasterLogDateTimeTextInputText.lower() in str(x[0]).lower()
            condition = condition and MasterLogPlaneIDTextInputText.lower() in str(x[1]).lower()
            condition = condition and MasterLogNoteTextInputText.lower() in str(x[2]).lower()

            if condition:
                newData.append({'datetime': str(x[0]),
                                'planeID': str(x[1]),
                                'note': str(x[2])})
        self.ids.MasterLogList.rv.data = newData

# Class for a row of DepartureList, the list of departing planes
class MasterLogRow(RecycleDataViewBehavior,BoxLayout):
    datetime = StringProperty()
    note = StringProperty()
    planeID = StringProperty()
    def __init__(self, **kwargs):
        super(MasterLogRow, self).__init__(**kwargs)

class MasterLogList(BoxLayout):
    def __init__(self, **kwargs):
        global masterLogData
        super(MasterLogList, self).__init__(**kwargs)
        Clock.schedule_once(self.finish_init,0)

    # Autopopulate list of departures
    def finish_init(self, dt):
        self.populate()

    # Populate list of departures
    def populate(self):
        #Query will give results of table as rows of rows and tuples of contained objects
        query_result = master_log_access.get_Master_Log()
        self.masterLogData = query_result
        self.rv.data = [
            {'datetime': str(x[0]),
                'planeID': str(x[1]),
                'note': str(x[2])}
            for x in query_result]
    
    def refresh(self):
        query_result = master_log_access.get_Master_Log()
            
        self.rv.data = [
            {'datetime': str(x[0]),
                'planeID': str(x[1]),
                'note': str(x[2])}
            for x in query_result]

# 88 88b 88  dP""b8 88 8888b.  888888 88b 88 888888     88      dP"Yb   dP""b8 
# 88 88Yb88 dP   `" 88  8I  Yb 88__   88Yb88   88       88     dP   Yb dP   `" 
# 88 88 Y88 Yb      88  8I  dY 88""   88 Y88   88       88  .o Yb   dP Yb  "88 
# 88 88  Y8  YboodP 88 8888Y"  888888 88  Y8   88       88ood8  YbodP   YboodP 

class IncidentLogWindow(Screen):
    def search(self):
        # Getting the text values from text inputs
        IncidentLogDatetimeTextInputText = self.ids.IncidentLogDatetimeTextInput.text
        IncidentLogCodeTextInputText = self.ids.IncidentLogCodeTextInput.text
        IncidentLogNoteTextInputText = self.ids.IncidentLogNoteTextInput.text

        # make a new dataset based on search terms
        newData = []
        for x in getattr(self.ids.IncidentLogList, 'incidentLogData'):
            # Ensure that row matches search criteria
            condition = True
            condition = condition and IncidentLogDatetimeTextInputText.lower() in str(x[0]).lower()
            condition = condition and IncidentLogCodeTextInputText.lower() in str(x[1]).lower()
            condition = condition and IncidentLogNoteTextInputText.lower() in str(x[2]).lower()

            if condition:
                newData.append({'datetime': str(x[0]),
                                'code': str(x[1]),
                                'note': str(x[2])})
        self.ids.IncidentLogList.rv.data = newData

# Class for a row of DepartureList, the list of departing planes
class IncidentLogRow(RecycleDataViewBehavior,BoxLayout):
    datetime = StringProperty()
    code = StringProperty()
    note = StringProperty()
    def __init__(self, **kwargs):
        super(IncidentLogRow, self).__init__(**kwargs)

class IncidentLogList(BoxLayout):
    def __init__(self, **kwargs):
        global incidentLogData
        super(IncidentLogList, self).__init__(**kwargs)
        Clock.schedule_once(self.finish_init,0)

    # Autopopulate list of departures
    def finish_init(self, dt):
        self.populate()

    # Populate list of departures
    def populate(self):
        #Query will give results of table as rows of rows and tuples of contained objects
        query_result = incident_log_access.get_Incident_Logs()
        
        self.incidentLogData = query_result

        self.rv.data = [
            {'datetime': str(x[0]),
             'code': str(x[1]),
             'note': str(x[2])}
            for x in query_result]
            
    def refresh(self):
        query_result = incident_log_access.get_Incident_Logs()
            
        self.rv.data = [
            {'datetime': str(x[0]),
             'code': str(x[1]),
             'note': str(x[2])}
            for x in query_result]

#  dP""b8 88""Yb  dP"Yb  88   88 88b 88 8888b.       dP""b8 88""Yb 888888 Yb        dP     .dP"Y8 88 8b    d8 
# dP   `" 88__dP dP   Yb 88   88 88Yb88  8I  Yb     dP   `" 88__dP 88__    Yb  db  dP      `Ybo." 88 88b  d88 
# Yb  "88 88"Yb  Yb   dP Y8   8P 88 Y88  8I  dY     Yb      88"Yb  88""     YbdPYbdP       o.`Y8b 88 88YbdP88 
#  YboodP 88  Yb  YbodP  `YbodP' 88  Y8 8888Y"       YboodP 88  Yb 888888    YP  YP        8bodP' 88 88 YY 88 

class EngineeringCheckPopup(Popup):
    pass

class ExtendGatePopup(Popup):
    pass


class GroundCrewSimulationWindow (Screen):
    def engineeringCheck(self):
        h = self.ids.GroundCrewSimFloatLayout.height
        w = self.ids.GroundCrewSimFloatLayout.width

        anim1 = Animation(x=w*.68, y=h*.68, duration=1)
        anim1.start(self.ids.worker1)

        anim2 = Animation(x=w*.54, y=h*.33, duration=1)
        anim2.start(self.ids.worker2)

        anim3 = Animation(x=w*.65, y=h*.9, duration=1)
        anim3.start(self.ids.worker3)

        anim4 = Animation(x=w*.56, y=h*.54, duration=1)
        anim4.start(self.ids.worker4)

        anim5 = Animation(x=w*.73, y=h*.29, duration=1)
        anim5.start(self.ids.worker5)

        threading.Timer(3, self.createEngineeringCheckPopup).start()

    def createEngineeringCheckPopup(self):
        eCheckPopup = EngineeringCheckPopup(pos= (self.center_x - 150, self.center_y-100))
        eCheckPopup.open()

    def extendGate(self):
        h = self.ids.GroundCrewSimFloatLayout.height
        w = self.ids.GroundCrewSimFloatLayout.width

        # Move Workers
        anim1 = Animation(x=w*.02, y=h*.1, duration=1)
        anim1.start(self.ids.worker1)

        anim2 = Animation(x=w*.02, y=h*.15, duration=1)
        anim2.start(self.ids.worker2)

        anim3 = Animation(x=w*.02, y=h*.2, duration=1)
        anim3.start(self.ids.worker3)

        anim4 = Animation(x=w*.02, y=h*.25, duration=1)
        anim4.start(self.ids.worker4)

        anim5 = Animation(x=w*.02, y=h*.30, duration=1)
        anim5.start(self.ids.worker5)


        # Extend gate
        gateAnim = Animation(size_hint=(.03, .27), duration=3)
        gateAnim.start(self.ids.gate)

        threading.Timer(3, self.createExtendGatePopup).start()

    def createExtendGatePopup(self):
        gPopup = ExtendGatePopup(pos= (self.center_x - 150, self.center_y-100))
        gPopup.open()
        
    




#  dP""b8  dP"Yb  8b    d8 8b    d8 88   88 88b 88 88  dP""b8    db    888888 88  dP"Yb  88b 88 .dP"Y8 
# dP   `" dP   Yb 88b  d88 88b  d88 88   88 88Yb88 88 dP   `"   dPYb     88   88 dP   Yb 88Yb88 `Ybo." 
# Yb      Yb   dP 88YbdP88 88YbdP88 Y8   8P 88 Y88 88 Yb       dP__Yb    88   88 Yb   dP 88 Y88 o.`Y8b 
#  YboodP  YbodP  88 YY 88 88 YY 88 `YbodP' 88  Y8 88  YboodP dP""""Yb   88   88  YbodP  88  Y8 8bodP' 


class CommunicationsWindow (Screen):
    red = ListProperty([1, 0, 0, 1])
    green = ListProperty([0, 1, 0, 1])

    def bringDown(self):
        # You have to configure this as new channels are added
        numChannels = 5
        
        channelToBringDown = randint(1, numChannels)

        print("BRINGING DOWN CHANNEL " + str(channelToBringDown))

        if channelToBringDown == 1:
            self.ids.Channel1.ids.circle.source = "./resources/images/red.png"
            incident_log_access.add_Row('3', "Communication channel 1 down")
            Clock.schedule_once(self.make1Green, 3)

        if channelToBringDown == 2:
            self.ids.Channel2.ids.circle.source = "./resources/images/red.png"
            incident_log_access.add_Row('3', "Communication channel 2 down")
            Clock.schedule_once(self.make2Green, 3)

        if channelToBringDown == 3:
            self.ids.Channel3.ids.circle.source = "./resources/images/red.png"
            incident_log_access.add_Row('3', "Communication channel 3 down")
            Clock.schedule_once(self.make3Green, 3)

        if channelToBringDown == 4:
            self.ids.Channel4.ids.circle.source = "./resources/images/red.png"
            incident_log_access.add_Row('3', "Communication channel 4 down")
            Clock.schedule_once(self.make4Green, 3)

        if channelToBringDown == 5:
            self.ids.Channel5.ids.circle.source = "./resources/images/red.png"
            incident_log_access.add_Row('3', "Communication channel 5 down")
            Clock.schedule_once(self.make5Green, 3)


    def make1Green(self, dt):
        self.ids.Channel1.ids.circle.source = "./resources/images/green.png"
    def make2Green(self, dt):
        self.ids.Channel2.ids.circle.source = "./resources/images/green.png"
    def make3Green(self, dt):
        self.ids.Channel3.ids.circle.source = "./resources/images/green.png"
    def make4Green(self, dt):
        self.ids.Channel4.ids.circle.source = "./resources/images/green.png"
    def make5Green(self, dt):
        self.ids.Channel5.ids.circle.source = "./resources/images/green.png"

class ChannelRow(GridLayout):
    channel_text = StringProperty()
    def __init__(self, **kwargs):
        super(ChannelRow, self).__init__(**kwargs)

    def contactPilot(self, planeID):
        print("contacting pilot of plane " + str(planeID))
        master_log_access.add_Row("Contacted plane " + str(planeID), "", "0", int(planeID))

# Class for controller for simulated workers
class SimulatedWorkerAnimationController():
    pass

# Class for alert creator
class AlertCreator():
    pass

    # Create alert
