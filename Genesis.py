import random
import json
import os

# Note, class name attribute will be for the species to decide what it will be called

def main():
    pln = Planet("earth")
    pln.Simulate(100)
    print(getInitWeights("earth"))

def getInitWeights(planet):
    if os.path.exists(f"Init/{planet}.json"):
        with open(f"Init/{planet}.json", "r") as f:
            return json.load(f)

class Planet():
    def __init__(self, planet):
        weights = getInitWeights(planet)
        self.name = weights
        self.radius
        self.mass
        self.age
        self.gravity
        self.rotationPeriod
        self.orbitalPeriod
        self.distanceFromStar
        
        self.Layers = [Atmosphere(), Crust(), Mantle()]
        
    def Simulate(days):
        pass
        

class Atmosphere():
    def __init__(self):
        self.pollution
        self.color


class Crust():
    def __init__(self):
        self.Continents = self.genContinents()
        self.Oceans = self.getOceans()
        
    def genContinents():
        return ["North America", "Africa", "South America", "Asia"]
        
        
class Mantle():
    def __init__(self):
        self.Caves = self.genCaves()
        
    def genCaves():
        pass

        
        
class Continent():
    def __init__(self):
        self.name
        self.climate
        self.size
        
class Ocean():
    def __init__(self):
        self.name
        self.climate
        self.depth
        self.Life = self.genOceanLife()
        
    def genOceanLife():
        pass

class Convert():
    def __init__(self, measurement):
        if "lb" in measurement and "^" in measurement and "e" in measurement:
            pass
        
    def toMiles(distance):
        if distance.type == str:
            pass
        
        
        

main()