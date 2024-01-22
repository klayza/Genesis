import json
import random
import periodictable

class SimpleObject(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return {key: value for key, value in obj.__dict__.items() if not key.startswith("_")}
        return super().default(obj)


def to_dict(obj):
    return json.loads(json.dumps(obj, cls=SimpleObject, indent=4))


class Base:
    def __init__(self, parent=None):
        self.location = Location(self, parent)
        self.age = 0

    def update(self):
        self.age += 1

    def find_ancestor_of_type(self, ancestor_type):
        """Find the first ancestor of a given type."""
        loc = self.location
        while loc.parent is not None:
            if isinstance(loc.parent, ancestor_type):
                return loc.parent
            loc = loc.parent.location
        return None

    def add_child(self, child):
        if not hasattr(self, 'children'):
            self.children = []
        self.children.append(child)


class Location:
    def __init__(self, current, parent):
        self.current = current
        self.parent = parent
        if parent:
            parent.add_child(self.current)

# Universe and its children classes


class Universe(Base):
    def __init__(self):
        super().__init__()
        self.galaxies = [Galaxy(self) for _ in range(3)]

    def update(self):
        super().update()
        for galaxy in self.galaxies:
            galaxy.update()

        # self.age += 1

    def simulate(self, steps):
        for _ in range(steps):
            self.update()


class Galaxy(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = 1
        self.solar_systems = [SolarSystem(self) for _ in range(2)]

    def update(self):
        super().update()
        for solar_system in self.solar_systems:
            solar_system.update()


class SolarSystem(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.planets = [Planet(self) for _ in range(2)]
        self.suns = [Sun(self) for _ in range(1)]
        # actually like 1,390,000 in our solar system
        self.asteroids = [Asteroid(self) for _ in range(100)]

    def update(self):
        super().update()
        for sun in self.suns:
            sun.update()

        for planet in self.planets:
            planet.update()

        for asteroid in self.asteroids:
            asteroid.update()


    




class Sun(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mass = 100
        self.gravity = self.mass / 10  # example
        self.composition = [Element("hydrogen")]

    def update(self):
        super().update()


class Asteroid(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mass = random.randint(1, 15)

    def update(self):
        super().update()
        if random.randint(0, 11) == 5:  # 1 in 10
            ss = self.find_ancestor_of_type(SolarSystem)
            if ss:
                self.collide_with(random.choice(ss.planets))

    def collide_with(self, obj):
        obj.meteors.append(self)
        # TODO: appending meteors to a planet object  means that we will have to determine if the planet
        # will be able to stop it or not. There might not be explicit code for all things related to this, but I think it would be wise
        # to setup an event class so that we can add an event to the planet and if nothing is done if x amount of steps then an action will
        # be made. That action be defined in the event object.
        #
        # Ex:
        # Asteroid incoming to planet. Next step the planet acknowledges the event and if they
        # | have the power they can act upon it. The bottom line here is an asteroid doesn't dictate something's fate. The planet does
        #
        #


class Planet(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mass = random.randint(10, 30)
        self.gravity = self.mass / 2
        self.crust = Crust(self)
        self.atmosphere = Atmosphere(self)
        self.mantle = Mantle(self)
        self.destroyed = False
        self.meteors = []

    def update(self):
        super().update()
        self.atmosphere.update()
        self.crust.update()
        self.mantle.update()


class Atmosphere(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pollution = 0


class Mantle(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.caves = [Cave() for _ in range(100)]

    def update(self):
        super().update()
        for cave in self.caves:
            cave.update()


class Cave(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.life = [Life(self, "zombie") for _ in range(3)]
        self.volume = random.randint(100, 1000)
        self.exposed = random.randint(1, 100) < 10

    def update(self):
        super().update()
        # If there is an opening in the cave and 1 / 10
        if self.exposed and random.randint(1, 100) < 10:
            crust = self.find_ancestor_of_type(Crust)
            # Select a random life to fall into the cave
            if crust:
                town = crust.towns[random.randint(0, len(crust.towns))]
                life = town.life[random.randint(0, len(town.life))]
                self.life.append(life)
            else:
                # When a cave might be generated within the mantle
                pass

        for life in self.life:
            life.update()


class Crust(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.towns = [Town(self) for _ in range(2)]
        self.caves = [Cave() for _ in range(100)]
        self.meteorites = []

    def update(self):
        super().update()
        for town in self.towns:
            town.update()
        for cave in self.caves:
            cave.update()


class Town(Base):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.population = 1000
        self.life = [Life(self, "Human") for _ in range(100)]
        self.food = random.randint(0, 100)

    def update(self):
        super().update()
        self.make_food()
        for li in self.life:
            li.update()
            if li.deceased:
                self.population -= 1

    def make_food(self):
        make_food = self.population * 1
        self.food += make_food

class Element:
    def __init__(self, name="", symbol=None, atomic_number=None, atomic_weight=None, covalent_radius=None):

        # If the name or number not specified
        element = None
        if name: element = self.name_to_element(name)
        elif atomic_number: element = self.number_to_element(atomic_number)
        else: element = self.number_to_element(random.randint(1, 119))
        
        if not element:
            element = self.number_to_element(5)

        # Check for none in cr. Replace with 0 
        if element.covalent_radius == None: 
            element.covalent_radius = 0

        # Set values
        self.name = element.name
        self.symbol = element.symbol
        self.atomic_number = element.number
        self.atomic_weight = element.mass  
        self.covalent_radius = element.covalent_radius

    def name_to_element(self, name):
        return getattr(periodictable, name.lower())
    
    def number_to_element(self, number):
        for el in periodictable.elements:
            if el.number == number:
                return el


class Life(Base):
    # def __init__(self, parent, composition=[], species_name=""):
    #     super().__init__(parent)
    def __init__(self, composition=[], species_name=""):

        self.composition = composition
        

        if species_name != "":
            self.composition = self.name_to_composition(species_name)

        elif len(composition) < 1:
            self.composition = self.env_to_composition()

        ### Foundational traits ###
        self.mobility = round(self.calculate_trait('atomic_number'))
        self.reactivity = round(self.calculate_trait('atomic_weight'))
        self.reproduction = round(self.calculate_trait('covalent_radius'))
        self.longevity = round(self.calculate_trait('atomic_number'))
        self.consumption = round(self.calculate_trait('atomic_weight'))
        self.resistance = round(self.calculate_trait('covalent_radius'))

        ### Foundational Properties ###
        self.id = '.'.join([str(element.atomic_number) for element in self.composition])
        self.gene = self.encode_gene()
        self.overall = self.mobility + self.reactivity + self.reproduction + self.longevity + self.consumption + self.resistance

        ### Gained Traits ###
        # traits that must be met by certain conditions #
        self.happiness = None
        self.consciousness = None
        self.intelligence = None

        ### Initial Traits ###
        self.deceased = False

        ### Current Stats ###
        self.energy = (self.mobility * self.resistance) / self.consumption
        self.health = self.resistance * self.reactivity
        # self.

    def update(self):
        if self.deceased: return
        super().update()
        if self.hungry: self.find_food()


    def encode_gene(self):
        keys = {
            "mobility": self.mobility,
            "reactivity": self.reactivity,
            "reproduction": self.reproduction,
            "longevity": self.longevity,
            "consumption": self.consumption,
            "resistance": self.resistance,
        }
        return ".".join([((3 - len(str(keys[key]))) * "0") + str(keys[key]) for key in keys])


    def env_to_composition(self):
        """Find the planets 3 most common elements. Returns a list of elements"""
        planet = self.find_ancestor_of_type(Planet)
        if planet:
            return planet.composition[:3]
        # If this life form isn't on a planet!!??
        else:
            # NYI - find the life's closest parent env. Might be an asteroid, interstellar spaceship
            pass

    def name_to_composition(self, name):
        """For defining species. Returns a list of elements"""
        name = name.lower()
        if name == "human":
            return [Element(name="hydrogen"), Element(name="carbon"), Element(name="lead")]
        elif name == "zombie":
            return [Element(name="iron"), Element(name="uranium"), Element(name="carbon")]
        elif name == "khaar":
            pass
        elif name == "scp-321":
            pass
    
    def calculate_trait(self, property_name):
        return sum([getattr(element, property_name) for element in self.composition])
    
    def print(self):
        print(self.id, end="  ")
        print(self.mobility, end="  ")
        print(self.reactivity, end="  ")
        print(self.reproduction, end="  ")
        print(self.longevity, end="  ")
        print(self.consumption, end="  ")
        print(self.resistance, end="  ")
        print("---", end="  ")
        print(self.overall, end="  ")
        print("")


    def update(self):
        super().update()

# for i in range(10):
#     l = Life(composition=[Element() for _ in range(3)])
#     # l = Life(species_name="zombie")
#     print(l.gene)
#     # l.print()
# exit()

# uni = Universe()
# uni.simulate(1)
# for life in uni.galaxies[0].solar_systems[0].planets[0].crust.towns[0].life:
#     print(life.gene, life.age, life.strength +
#           life.stamina + life.intelligence, life.deceased)
# exit()

# EXAMPLE USAGE
###########################################################
# Create a Universe with nested objects
universe = Universe()
# Grab a sample Town
sample_town = universe.galaxies[0].solar_systems[0].planets[0].crust.towns[0]
# Test find_ancestor_of_type
found_planet = sample_town.find_ancestor_of_type(Planet)
found_universe = sample_town.find_ancestor_of_type(Universe)

print("Found Planet:", found_planet is not None)
print("Found Universe:", found_universe is not None)
###########################################################


def getLife(universe):
    residents = []
    for galaxy in universe.galaxies:
        # print("---")
        # print(galaxy.name)
        for solar_system in galaxy.solar_systems:
            for planet in solar_system.planets:
                for town in planet.crust.towns:
                    for resident in town.life:
                        residents.append(resident)

    return residents


life = getLife(Universe())
for l in life:
  l.print()
  c = l.find_ancestor_of_type(Planet).composition
  print(c)
