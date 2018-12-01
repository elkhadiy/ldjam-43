import uuid
import random


class CrewMember():

    def __init__(self, name, stats, skills, consumption, state):
        self.name = name
        self.skills = skills
        self.consumption = consumption
        self.state = state
        self.stats = stats
