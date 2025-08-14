from utils.node import Node
from tkinter import messagebox

class Valve(Node):
    connections = []
    directions = 0
    def __init__(self, ein, pit = None, jumper = None, field_label = None, connections_set_id = None, dvi = None):
        super().__init__(ein, pit= pit, jumper = jumper, field_label= field_label, connections_set_id = connections_set_id) 
        self.connections
        self.directions
        self.show = True
        self.in_tank = False
        self.jumper = jumper
        self.dvi_credited = dvi

                
        