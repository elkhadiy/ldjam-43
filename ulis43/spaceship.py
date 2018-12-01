
class Spaceship():

    def __init__(self, ressources, crew, rooms):
        self.ressources = ressources
        self.crew = crew
        self.rooms = rooms

    def __repr__(self):
        return """Ressources: {}\nCrew: {}\nRooms: {}\n""".format(
            self.ressources, self.crew, self.rooms
        )
