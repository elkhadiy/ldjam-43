class CrewMember():

    def __init__(self, name, stats, skills, consumption, state):
        self.name = name
        self.skills = skills
        self.consumption = consumption
        self.state = state
        self.stats = stats
        self.x = 0
        self.y = 0

    def tick(self, global_ressources):
        if self.state != "NOMINAL":
            self.stats["hp"] -= 1
        if self.stats["hp"] <= 0:
            self.state = "OUT_OF_SERVICE"
        if self.state != "OUT_OF_SERVICE":
            for ressource in ["OXYGEN", "WATER", "FOOD"]:
                if global_ressources[ressource]:
                    global_ressources[ressource] = max(0, global_ressources[ressource] - 1)
                else:
                    self.stats["hp"] -= 1
        return global_ressources

    def draw(self, ctx):
        pass

    def __repr__(self):
        return """Name: {}
        Skills: {}
        Consumption: {}
        State: {}
        Stats: {}\n""".format(
            self.name, self.skills,
            self.consumption, self.state,
            self.stats
            )
