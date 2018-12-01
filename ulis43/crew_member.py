class CrewMember():

    def __init__(self, name, stats, skills, consumption, state):
        self.name = name
        self.skills = skills
        self.consumption = consumption
        self.state = state
        self.stats = stats

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
