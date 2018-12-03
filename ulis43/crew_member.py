import yaml
import random

import ulis43
from ulis43.asset_manager import AssetManager

class CrewMember():

    def __init__(self, name, stats, skills, consumption, state):
        self.name = name
        self.skills = skills
        self.consumption = consumption
        self.state = state
        self.stats = stats

        self.pos = (0, 0)

        self.bodyparts = {}


        dominant_skill = max(skills, key=skills.get)

        res_folder = ulis43.basedir / "res"
        crew_appearance_file = res_folder / "crew_appearance.yaml"
        with crew_appearance_file.open() as f:
            crew_appearance = yaml.safe_load(f)



        self.bodyparts["skill"] = "skills_" + random.choice(crew_appearance["skills"][dominant_skill])

        self.bodyparts["head"] = "heads_" +  random.choice(crew_appearance["images"]["heads"])
        self.skincolor = random.choice(crew_appearance["colors"]["skin"])

        self.bodyparts["hair"] = "hairs_" +  random.choice(crew_appearance["images"]["hairs"])
        self.haircolor = random.choice(crew_appearance["colors"]["hair"])

        self.bodyparts["face"] = "faces_" +  random.choice(crew_appearance["images"]["faces"])
        self.eyecolor = random.choice(crew_appearance["colors"]["eye"])

        self.bodyparts["body"] = "bodies_" + self.stats["shape"]
        self.skillcolor = crew_appearance["colors"]["skills"][dominant_skill]

    def tick(self, global_ressources):
        if self.state == "OUT_OF_SERVICE":
            return global_ressources

        if self.state != "NOMINAL":
            self.stats["hp"] -= 1
        if self.stats["hp"] <= 0:
            for stat in self.stats.keys():
                self.stats[stat] = 0
            self.skincolor = (75,45,175)
            self.state = "OUT_OF_SERVICE"
        if self.state != "OUT_OF_SERVICE":
            for ressource in ["OXYGEN", "WATER", "FOOD"]:
                if global_ressources[ressource]:
                    global_ressources[ressource] = max(0, global_ressources[ressource] - 1)
                else:
                    self.stats["hp"] -= 1

        x, y = self.pos
        x += random.randint(-1,1)
        y += 1 - random.randint(0,2)

        x = (x//100)*100 + max(min(x % 100, 70), 10)
        y = (y//100)*100 + max(min(y % 100, 60), 10)
        self.pos = (x, y)

        return global_ressources

    def draw(self, ctx):
        ctx.blit(AssetManager().getColoredImage(self.bodyparts["body"], self.skillcolor), self.pos)
        ctx.blit(AssetManager().getColoredImage(self.bodyparts["head"], self.skincolor), self.pos)
        ctx.blit(AssetManager().getColoredImage(self.bodyparts["face"], self.eyecolor), self.pos)
        ctx.blit(AssetManager().getColoredImage(self.bodyparts["hair"], self.haircolor), self.pos)
        ctx.blit(AssetManager().getImage(self.bodyparts["skill"]), self.pos)

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
