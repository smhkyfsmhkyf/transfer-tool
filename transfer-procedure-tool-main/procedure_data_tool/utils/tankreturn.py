from utils.node import Node
from tkinter import messagebox

class TankReturn(Node):
    directions = 1
    def __init__(self, ein, pit = None, jumper = None, field_label = None, connections_set_id = None, dvi = None):
        super().__init__(ein, pit, jumper, field_label= field_label, connections_set_id = connections_set_id) 
        self.ein = ein
        self.directions = 1 
        self.node_1 = None
        self.connections = []
        self.show = True
        self.dvi_credited 
        self.dvi_used = False
        self.in_tank = True
        self.color = "lightgreen"
   
       
        # HAVE EIN OUTPUT JUST THE LABEL (Last character)?
        def EIN(self):
            return self.ein[-1]
        

        def linkDVI(self, caller = None, stop = False):
            dvi_items = []
            return dvi_items

