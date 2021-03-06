import yaml
import random
import pygame

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
        self.drawpos = (0, 0)
        self.rotation = 0
        self.drawrotation = 0

        self.grabbed = False
        self.current_room = None

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
        if not self.grabbed and self.current_room and not self.state == "OUT_OF_SERVICE":

            x += random.randint(-15,15)
            y += random.randint(-15,15)

            x = self.current_room.pos[0] + max(min((x - self.current_room.pos[0]) % 100, 99-(32+5)), 5)
            y = self.current_room.pos[1] + max(min((y - self.current_room.pos[1]) % 100, 99-(32+5)), 5)

            self.pos = (x, y)

        if not self.current_room:
            self.pos = (x + 15, y)
            self.rotation += 5

        return global_ressources

    def draw(self, ctx):
        x, y = self.pos
        drx, dry = self.drawpos

        self.drawpos = ( drx + (-1 if drx - x > 0 else 1 if drx - x < 0 else 0),
                         dry + (-1 if dry - y > 0 else 1 if dry - y < 0 else 0))

        if self.grabbed and self.current_room:
            x, y = pygame.mouse.get_pos()
            self.drawpos = (x - 16, y - 16)

        ctx.blit(pygame.transform.rotate(AssetManager().getColoredImage(self.bodyparts["body"], self.skillcolor), self.rotation), self.drawpos)
        ctx.blit(pygame.transform.rotate(AssetManager().getColoredImage(self.bodyparts["head"], self.skincolor), self.rotation), self.drawpos)
        ctx.blit(pygame.transform.rotate(AssetManager().getColoredImage(self.bodyparts["face"], self.eyecolor), self.rotation), self.drawpos)
        ctx.blit(pygame.transform.rotate(AssetManager().getColoredImage(self.bodyparts["hair"], self.haircolor), self.rotation), self.drawpos)
        ctx.blit(pygame.transform.rotate(AssetManager().getImage(self.bodyparts["skill"]), self.rotation), self.drawpos)

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
