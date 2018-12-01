class Room():

    def __init__(self, type, capacity, hp, efficiency, state="NOMINAL"):
        self.type = type
        self.capacity = capacity
        self.hp = hp
        self.efficiency = efficiency
        self.state = state

    def tick(self, spaceship_state):
        pass

    def __repr__(self):
        return """Type: {}
        Capacity: {}
        HP: {}
        Efficiency: {}
        State: {}\n""".format(
            self.type, self.capacity, self.hp, self.efficiency, self.state
            )
