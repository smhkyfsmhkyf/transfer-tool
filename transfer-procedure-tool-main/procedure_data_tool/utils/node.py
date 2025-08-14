from collections import deque
from tkinter import messagebox

class Node:
    connections = []
    directions = 0
    pit = None
    jumper = None
    jumperLabel = None
    position = None
    onJumper = True
    dvi_credited = None
    dvi_used = None
    in_tank = False
    color = 'lightgray'
    size = 50
    field_label = None
    connections_set_id = None
    def __init__(self, ein, pit, jumper, field_label, connections_set_id):
        self.ein = ein
        self.pit = pit
        self.jumper = jumper
        self.field_label = field_label
        self.connections_set_id = connections_set_id
        self.directions
        self.connections
        # self.dvi_used
        self.show = True
        self.in_tank = False
        self.dvi_credited = None
        self.dvi_used = None
        self.jumperLabel
        self.position
        self.onJumper
        self.color
        # self.size
    
    def EIN(self):
        return self.ein
    
    def __str__(self):
        return self.ein
    
    def setPit(self, str):
        self.pit = str

    def setJumper(self, jumper):
        self.jumper = jumper
    
    def setConnectionSetID(self, connections_set_id):
        self.connections_set_id = connections_set_id
    
    
    def linkDVI(self, caller = None, stop = False):
        dvi_items = [self]
        for connection in self.connections:
            if connection == caller:
                pass
            else: 
                dvi_items.extend(connection.linkDVI(caller = self))
        if len(dvi_items) == 1:
            return []
        return dvi_items
    
    def setPosition(self, route = None, forced = None):
        return
    
    def getColor(self):
        return self.color

    ###connectBack is to allow for bidirectional connectivity
    def connectBack(self, node):
        if node in self.connections: 
            return
        ###directions is the maximum number of connections ? 
        elif len(self.connections) < self.directions: 
            self.connect(node)
        else: 
            print(self.EIN(), "has maximum number of connections, cant connect back")
            print(type(self))
            for con in self.connections:
                print(con.EIN())
        return

    ###This allows adding more nodes
    def connect(self, *nodes):
        #slices the connections list up to the maximum number of connections ?
        for node in nodes[:self.directions]:
            #checks if the node exists, and if it's not already in the connections list, then it adds it.
            if node and node not in self.connections:
                #if there is room in the list, then add  the node.
                if len(self.connections) <= self.directions:
                    self.connections.append(node)
                    #Calls connectBack() to make it bidirectional
                    node.connectBack(self)
                else:  
                    print("has maximum number of connections", self.EIN())
                    for connection in self.connections:
                        print(connection.EIN())

    def report(self):
        print((self.EIN()), "connections: ")
        for node in self.connections:
            if (node):
                print(node.EIN())
            else:
                print("Missing Connection")
    
    def routesTo(self, target, num_routes = 1, exclude_target = None):
        paths = []
        queue = deque([[self]])

        while queue and len(paths) < num_routes:
            path = queue.popleft()
            node = path[-1]

            if node == target:
                if path not in paths:
                    paths.append(path)
                
            for connection in node.connections :
                if connection not in path and (exclude_target is None or exclude_target not in path):
                    queue.append(path + [connection])

        return paths