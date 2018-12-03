import random

from ulis43.asset_manager import AssetManager


class Room():

    def __init__(self, type, capacity, hp, efficiency, state="NOMINAL"):
        self.type = type
        self.capacity = capacity
        self.hp = hp
        self.efficiency = efficiency
        self.state = state
        self.neighbours = {
            "left": None,
            "right": None,
            "top": None,
            "down": None
        }
        # not a set because too lazy to make hashable stuff
        self.staff = []
        self.pos = (0, 0)

    def add_crew_member(self, crew_member, pos=None):
        if len(self.staff) < self.capacity or self.type == "HQ":
            if pos:
                crew_member.pos = pos
            else:
                crew_member.pos = (random.randint(self.pos[0] + 20, self.pos[0] + 80),
                                   random.randint(self.pos[1] + 20, self.pos[1] + 60))
            self.staff.append(crew_member)

        return len(self.staff) < self.capacity

    def remove_crew_member(self, crew_member):
        if len(self.staff):
            self.staff.remove(crew_member)

    def set_neighbour(self, room, pos):
        if pos in ["left", "right", "top", "down"]:
            self.neighbours[pos] = room

    # note(elk): Use childclasses ?
    #            but then I can't conviniently just call Room(**yaml_data)
    #            and get the child class I would expect

    def tick(self, global_ressources):

        # Resolve ressource creation and consumption

        if self.type == "WATER_PLANT":
            global_ressources = self.__water_plant_tick(global_ressources)
        elif self.type == "OXYGEN_PLANT":
            global_ressources = self.__oxygen_plant_tick(global_ressources)
        elif self.type == "FARMING_PLANT":
            global_ressources = self.__farming_plant_tick(global_ressources)
        elif self.type == "ELECTRICAL_PLANT":
            global_ressources = self.__electrical_plant_tick(global_ressources)
        elif self.type == "MACHINE_ROOM":
            global_ressources = self.__machine_room_tick(global_ressources)
        elif self.type == "HQ":
            global_ressources = self.__hq_tick(global_ressources)

        global_ressources = self.__neighbour_effect_tick(global_ressources)

        return global_ressources

    def __water_plant_tick(self, global_ressources):
        if self.state == "NOMINAL":
            if global_ressources["ELECTRICITY"]:
                living_staff = [s for s in self.staff if s.stats["hp"]]
                global_ressources["ELECTRICITY"] = max(0, global_ressources["ELECTRICITY"] - 1)
                global_ressources["WATER"] += min(
                    int(self.efficiency / 100.0 * (
                        sum(map(lambda x: x.skills["CHEMISTRY"],   living_staff)) * 4 +
                        sum(map(lambda x: x.skills["ENGINEERING"], living_staff)) * 2
                        )),
                        20
                    )
        elif self.state == "ON_FIRE":
            pass
        elif self.state == "FLOODED":
            pass
        elif self.state == "BREACHED":
            pass
        else:  # self.state == "OUT_OF_SERVICE":
            pass
        return global_ressources

    def __oxygen_plant_tick(self, global_ressources):
        if self.state == "NOMINAL":
            if global_ressources["ELECTRICITY"] and global_ressources["WATER"]:
                living_staff = [s for s in self.staff if s.stats["hp"]]
                global_ressources["ELECTRICITY"] = max(0, global_ressources["ELECTRICITY"] - 1)
                global_ressources["WATER"]       = max(0, global_ressources["WATER"]       - 1)
                global_ressources["OXYGEN"] += min(
                    int(self.efficiency / 100.0 * (
                        sum(map(lambda x: x.skills["CHEMISTRY"]  , living_staff)) * 4 +
                        sum(map(lambda x: x.skills["ENGINEERING"], living_staff)) * 2
                        )),
                        20
                    )
        elif self.state == "ON_FIRE":
            pass
        elif self.state == "FLOODED":
            pass
        elif self.state == "BREACHED":
            pass
        else:  # self.state == "OUT_OF_SERVICE":
            pass
        return global_ressources

    def __farming_plant_tick(self, global_ressources):
        if self.state == "NOMINAL":
            if global_ressources["ELECTRICITY"] and global_ressources["WATER"]:
                living_staff = [s for s in self.staff if s.stats["hp"]]
                global_ressources["ELECTRICITY"] = max(0, global_ressources["ELECTRICITY"] - 1)
                global_ressources["WATER"]       = max(0, global_ressources["WATER"]       - 2)
                global_ressources["FOOD"] += min(
                    int(self.efficiency / 100.0 * (
                        sum(map(lambda x: x.skills["FARMING"],   living_staff)) * 4 +
                        sum(map(lambda x: x.skills["COOKING"],   living_staff)) * 2 +
                        sum(map(lambda x: x.skills["CHEMISTRY"], living_staff))
                        )),
                        20
                    )
                global_ressources["OXYGEN"] += min(
                    int(self.efficiency / 100.0 * (
                        sum(map(lambda x: x.skills["CHEMISTRY"], self.staff))
                        )),
                        20
                    )
        elif self.state == "ON_FIRE":
            pass
        elif self.state == "FLOODED":
            pass
        elif self.state == "BREACHED":
            pass
        else:  # self.state == "OUT_OF_SERVICE":
            pass
        return global_ressources

    def __electrical_plant_tick(self, global_ressources):
        if self.state == "NOMINAL":
            if global_ressources["WATER"]:
                living_staff = [s for s in self.staff if s.stats["hp"]]
                global_ressources["WATER"] = max(0, global_ressources["WATER"] - 1)
                global_ressources["ELECTRICITY"] += min(
                    int(self.efficiency / 100.0 * (
                        sum(map(lambda x: x.skills["ENGINEERING"], living_staff)) * 4 +
                        sum(map(lambda x: x.skills["CHEMISTRY"],   living_staff)) * 2
                        )),
                        20
                    )
        elif self.state == "ON_FIRE":
            pass
        elif self.state == "FLOODED":
            pass
        elif self.state == "BREACHED":
            pass
        else:  # self.state == "OUT_OF_SERVICE":
            pass
        return global_ressources

    def __machine_room_tick(self, global_ressources):
        if self.state == "NOMINAL":
            global_ressources["OXYGEN"]      = max(0, global_ressources["OXYGEN"]      - 2)
            global_ressources["ELECTRICITY"] = max(0, global_ressources["ELECTRICITY"] - 1)
        elif self.state == "ON_FIRE":
            pass
        elif self.state == "FLOODED":
            pass
        elif self.state == "BREACHED":
            pass
        else:  # self.state == "OUT_OF_SERVICE":
            pass
        return global_ressources

    def __hq_tick(self, global_ressources):
        if self.state == "NOMINAL":
            for ressource in ["OXYGEN", "WATER", "FOOD"]:
                if not global_ressources[ressource]:
                    self.hp = max(0, self.hp - 1)
            global_ressources["OXYGEN"]      = max(0, global_ressources["OXYGEN"]      - 1)
            global_ressources["WATER"]       = max(0, global_ressources["WATER"]       - 1)
            global_ressources["FOOD"]        = max(0, global_ressources["FOOD"]        - 1)
            global_ressources["ELECTRICITY"] = max(0, global_ressources["ELECTRICITY"] - 1)
        elif self.state == "ON_FIRE":
            pass
        elif self.state == "FLOODED":
            pass
        elif self.state == "BREACHED":
            pass
        else:  # self.state == "OUT_OF_SERVICE":
            pass
        return global_ressources

    def __neighbour_effect_tick(self, global_ressources):
        for neighbour in self.neighbours.values():
            if neighbour and neighbour.state == "NOMINAL":
                pass
            elif neighbour and neighbour.state == "ON_FIRE":
                pass
            elif neighbour and neighbour.state == "FLOODED":
                pass
            elif neighbour and neighbour.state == "BREACHED":
                pass
            else:  # neighbour and neighbour.state == "OUT_OF_SERVICE":
                pass

        # Room state mutation attempt

            # Probability to catch fire

            # Probability to get flooded

            # Probability to get breached

        return global_ressources

    def draw(self, ctx):
        ctx.blit(AssetManager().getImage(self.type), self.pos)

    def __repr__(self):
        return """Type: {}
        Capacity: {}
        HP: {}
        Efficiency: {}
        State: {}\n""".format(
            self.type, self.capacity, self.hp, self.efficiency, self.state
            )
