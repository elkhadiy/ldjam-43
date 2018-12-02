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
        self.x = 0
        self.y = 0

        self.pos = (random.randint(0,500), random.randint(0,500))

        self.bodyparts = {}


        dominant_skill = max(skills, key=skills.get)

        res_folder = ulis43.basedir / "res"
        crew_appearance_file = res_folder / "crew_appearance.yaml"
        with crew_appearance_file.open() as f:
            crew_appearance = yaml.safe_load(f)



        self.bodyparts["skill"] = "skills_" + random.choice(crew_appearance["skills"][dominant_skill])

        self.bodyparts["body"] = "Skinny"
        self.bodycolor = crew_appearance["colors"]["skills"][dominant_skill]

        self.bodyparts["head"] = "heads_1"
        self.skincolor = random.choice(crew_appearance["colors"]["skin"])

        self.bodyparts["hair"] = "hairs_" +  random.choice(crew_appearance["images"]["hairs"])
        self.haircolor = random.choice(crew_appearance["colors"]["hair"])

        self.bodyparts["body"] = "bodies_" + self.stats["shape"]
        self.skillcolor = crew_appearance["colors"]["skills"][dominant_skill]

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

        ctx.blit(AssetManager().getColoredImage(self.bodyparts["body"], self.skillcolor), self.pos)
        ctx.blit(AssetManager().getColoredImage(self.bodyparts["head"], self.skincolor), self.pos)
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
