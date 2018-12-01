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

    def add_crew_member(self, crew_member):
        if len(self.staff) < self.capacity:
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
        else:  # self.type == "HQ":
            global_ressources = self.__hq_tick(global_ressources)

        global_ressources = self.__neighbour_effect_tick(global_ressources)

        return global_ressources

    def __water_plant_tick(self, global_ressources):
        if self.state == "NOMINAL":
            global_ressources["WATER"] += (
                self.efficiency / 100.0 * (
                    sum(map(lambda x: x["Skills"]["CHEMISTRY"], self.staff)) +
                    sum(map(lambda x: x["Skills"]["ENGINEERING"], self.staff)) / 2
                    ) / 100.0
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
            global_ressources["OXYGEN"] += (
                self.efficiency / 100.0 * (
                    sum(map(lambda x: x["Skills"]["CHEMISTRY"], self.staff)) +
                    sum(map(lambda x: x["Skills"]["ENGINEERING"], self.staff)) / 2
                    ) / 100.0
                )
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

    def __farming_plant_tick(self, global_ressources):
        if self.state == "NOMINAL":
            global_ressources["FOOD"] += (
                self.efficiency / 100.0 * (
                    sum(map(lambda x: x["Skills"]["FARMING"], self.staff)) +
                    sum(map(lambda x: x["Skills"]["CHEMISTRY"], self.staff)) / 4
                    ) / 100.0
                )
            global_ressources["OXYGEN"] += (
                self.efficiency / 100.0 * (
                    sum(map(lambda x: x["Skills"]["CHEMISTRY"], self.staff)) / 2
                    ) / 100.0
                )
            global_ressources["ELECTRICITY"] = max(0, global_ressources["ELECTRICITY"] - 1)
            global_ressources["WATER"] = max(0, global_ressources["WATER"] - 1)
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
            global_ressources["ELECTRICITY"] += (
                self.efficiency / 100.0 * (
                    sum(map(lambda x: x["Skills"]["ENGINEERING"], self.staff)) +
                    sum(map(lambda x: x["Skills"]["CHEMISTRY"], self.staff)) / 4
                    ) / 100.0
                )
            global_ressources["WATER"] = max(0, global_ressources["WATER"] - 1)
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
            global_ressources["OXYGEN"] = max(0, global_ressources["OXYGEN"] - 2)
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
            global_ressources["OXYGEN"] = max(0, global_ressources["OXYGEN"] - 1)
            global_ressources["WATER"] = max(0, global_ressources["WATER"] - 1)
            global_ressources["FOOD"] = max(0, global_ressources["FOOD"] - 1)
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
        pass

    def __repr__(self):
        return """Type: {}
        Capacity: {}
        HP: {}
        Efficiency: {}
        State: {}\n""".format(
            self.type, self.capacity, self.hp, self.efficiency, self.state
            )
