# Proof of concept for ensuring a robust system later on
# Time is in days
import random

solarFlareChance = 0.000035

au = 92960000000

class System:
    def __init__(self):
        self.Suns = [Sun()]
        self.Planets = [Planet()]
        self.time = 0
        
    def Simulate(self, time):
        for Sun in self.Suns:
            Sun.Simulate(time)

class Sun:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.time = 0
        self.temp = 10000
        self.mass = 500000
        self.composition = [Element("hydrogen"), Element("helium")]
        self.Events = []

    def Simulate(self, time):
        for day in range(time):
            isSolarFlare = rollDice(solarFlareChance)
            if(isSolarFlare): self.Events.append(Event("Solar Flare", day, self.x, self.y))
            
class Planet:
    def __init__(self):
        init = getWeights("def.init.planet")
        self.x = init["x"]
        self.y = init["y"]
        

class Element:
    def __init__(self, name):
        self.name = name
        
class Event:
    def __init__(self, name, time, x, y):
        self.name = name
        self.time = time
        self.x = x
        self.y = y

# obj == weights class.class type.class object
# classes == [def, earth, or custom]
# types == [initial weights, or runtime weights]
#
def getWeights(obj):
    objects = getAllObjects()
    parts = obj.split(".")
    if(parts[0] == "def"):
        pass
    elif(parts[1] == "init"):
        pass
    elif(parts[2] in objects):
        pass
        
# Returns all of the possible objects in the game        
def getAllObjects():
    pass

        
    

def rollDice(chance):
    return random.uniform(-abs(chance), chance)

ss = System()
