import yaml


class Room():

    def __init__(self, type, capacity, hp, efficiency, state="NOMINAL"):
        self.type = type
        self.capacity = capacity
        self.hp = hp
        self.efficiency = efficiency
        self.state = state

    def tick(self, spaceship_state):
        pass
