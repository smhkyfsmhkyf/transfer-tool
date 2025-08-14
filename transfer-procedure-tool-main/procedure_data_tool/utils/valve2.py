from utils.valve import Valve
from utils.split import Split
from tkinter import messagebox


### Category for 2-way valves

class Valve2(Valve):
    directions = 2
    def __init__(self, ein, pit = None, jumper = None, field_label = None, connections_set_id = None, dvi = None):
        super().__init__(ein, pit= pit, jumper = jumper, field_label= field_label, connections_set_id = connections_set_id) 
        self.ein = ein
        self.directions = 2 
        self.connections = []
        self.show = True
        self.in_tank = False
        self.position = "CLOSED"
        self.dvi_credited = dvi
        self.dvi_used = "NO"
    
    def setPosition(self, route = None, forced = None):
            if forced == "CLOSED":
                self.position = "CLOSED"
            else: 
                self.position = "OPEN"
    
    def linkDVI(self, caller = None, stop = False):
        dvi_items = [self]
        if type(caller) == Split and not stop:
             for connection in self.connections:
                  if connection != caller:
                       dvi_items.extend(connection.linkDVI(caller=self))
        self.setPosition(forced = "CLOSED")
        self.dvi_used = "YES"
        self.color = "steelblue"
        return dvi_items
    
