
class Spaceship():

    def __init__(self, ressources, crew, rooms):
        self.ressources = ressources
        self.crew = crew
        self.rooms = rooms

    def tick(self):
        for crew_member in self.crew:
            self.ressources = crew_member.tick(self.ressources)
        for room in self.rooms:
            self.ressources = room.tick(self.ressources)

    def draw(self, ctx):
        for room in self.rooms:
            room.draw(ctx)
        for crew_member in self.crew:
            crew_member.draw(ctx)

    def __repr__(self):
        return """Ressources: {}\nCrew: {}\nRooms: {}\n""".format(
            self.ressources, self.crew, self.rooms
        )
