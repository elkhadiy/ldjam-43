import yaml
import random

import pygame
from pygame.locals import *

import ulis43
import ulis43.rooms
import ulis43.spaceship
import ulis43.crew_member
from ulis43.asset_manager import AssetManager


class Game:

    def __init__(self, difficulty="easy"):

        res_folder = ulis43.basedir / "res"
        config_file = res_folder / "config.yaml"

        with config_file.open() as f:
            config = yaml.safe_load(f)
        self.config = config

        ship_config = config["difficulty"][difficulty]

        # Ship ressources

        ressources = ship_config["ressources"]

        # Ship rooms

        # todo: see how to autoload python classes with yaml correctly
        # !!python/object:ulis43.rooms.Room didn't work
        rooms = []
        for room in ship_config["rooms"]:
            rooms.append(ulis43.rooms.Room(**room))

        # setup random room positions
        # simple random walk from last node (snake layout)
        # (could be better by keeping track of all possible placements)

        positions = [(random.randint(2, 5), random.randint(2, 5))]

        for _ in range(len(rooms) - 1):
            adjacents = [
                [
                    (p[0] + 1, p[1]), (p[0], p[1] + 1),
                    (p[0] - 1, p[1]), (p[0], p[1] - 1)
                ]
                for p in positions
                ]
            adjacents = [item for sublist in adjacents for item in sublist]
            adjacents = [
                p for p in adjacents
                if p[0] >= 0 and p[0] <= 5 and p[1] >= 0 and p[1] <= 5
                ]
            adjacents = list(set(adjacents))
            adjacents = [p for p in adjacents if p not in positions]
            positions.append(random.sample(adjacents, 1)[0])
            random.shuffle(positions)

        min_x = min(positions, key=lambda p: p[0])[0] * 100
        min_y = min(positions, key=lambda p: p[1])[1] * 100
        max_x = max(positions, key=lambda p: p[0])[0] * 100
        max_y = max(positions, key=lambda p: p[1])[1] * 100
        center_x = (max_x + 100 - min_x) / 2 + min_x
        center_y = (max_y + 100 - min_y) / 2 + min_y
        delta_x = center_x - 300
        delta_y = center_y - 300

        positions = [(p[0] * 100 - delta_x, p[1] * 100 - delta_y) for p in positions]

        for i, room in enumerate(rooms):
            room.pos = positions[i]

        # Crew
        crew = []
        for _ in range(ship_config["crew_size"]):
            randroom = random.sample(rooms, 1)[0]
            new_crew = createCrew()
            crew.append(new_crew)
            randroom.add_crew_member(new_crew)

        # Instanciate spaceship

        self.spaceship = ulis43.spaceship.Spaceship(
            ressources=ressources,
            crew=crew,
            rooms=rooms
        )

        self.last_grabbed = None

        AssetManager().loadMusic("Mall", "Komiku_-_08_-_Mall.mp3")
        AssetManager().playMusic("Mall")

    def tick(self):
        if min(self.spaceship.ressources.values()) > 100:
            randroom = random.sample(self.spaceship.rooms, 1)[0]
            new_crew = createCrew()
            randroom.add_crew_member(new_crew)
            new_crew.current_room = randroom
            self.spaceship.crew.append(new_crew)

        self.spaceship.tick()

        alive = [staff for staff in self.spaceship.crew if staff.stats["hp"]]

        return not bool(alive)

    def draw(self, ctx):
        if pygame.mouse.get_pressed()[0] and not [member for member in self.spaceship.crew if member.grabbed]:
            pos = pygame.mouse.get_pos()
            self.grab_crew(pos)
        if not pygame.mouse.get_pressed()[0] and [member for member in self.spaceship.crew if member.grabbed]:
            pos = pygame.mouse.get_pos()
            self.grab_crew(pos)
        self.spaceship.draw(ctx)

        pos = pygame.mouse.get_pos()
        crew_member = [
            member
            for member in self.spaceship.crew
            if member.pos[0] <= pos[0] + 8 and pos[0] <= member.pos[0] + 24
            and member.pos[1] <= pos[1] + 8 and pos[1] <= member.pos[1] + 24
        ]
        if crew_member:
            crew_member = crew_member[0]
            name_surf, name_rect = AssetManager().getFont("hud").render(
                crew_member.name,
                fgcolor=(251, 242, 54)
            )
            hp_surf, hp_rect = AssetManager().getFont("hud").render(
                "HP: {}".format(crew_member.stats["hp"]),
                fgcolor=(255, 0, 0)
            )
            elec_surf, elec_rect = AssetManager().getFont("hud").render(
                "ENG: {0:.2f}".format(crew_member.skills["ENGINEERING"]),
                fgcolor=(251, 242, 54)
            )
            water_surf, water_rect = AssetManager().getFont("hud").render(
                "CHEM: {0:.2f}".format(crew_member.skills["COOKING"]),
                fgcolor=(99, 155, 255)
            )
            oxy_surf, oxy_rect = AssetManager().getFont("hud").render(
                "COOK: {0:.2f}".format(crew_member.skills["FARMING"]),
                fgcolor=(138, 111, 48)
            )
            food_surf, food_rect = AssetManager().getFont("hud").render(
                "FARM: {0:.2f}".format(crew_member.skills["CHEMISTRY"]),
                fgcolor=(138, 111, 48)
            )

            ctx.blit(name_surf, name_rect.move(600, 220))
            ctx.blit(hp_surf, hp_rect.move(600, 240))
            ctx.blit(elec_surf, elec_rect.move(600, 260))
            ctx.blit(water_surf, water_rect.move(600, 280))
            ctx.blit(oxy_surf, water_rect.move(600, 300))
            ctx.blit(food_surf, food_rect.move(600, 320))


    def grab_crew(self, pos):
        grabbed_crew_member = [
            member for member in self.spaceship.crew if member.grabbed
        ]
        if grabbed_crew_member:
            if not grabbed_crew_member[0].current_room:
                self.last_grabbed = None
                return
            self.last_grabbed = grabbed_crew_member[0]
            grabbed_crew_member[0].grabbed = False
            hovered_room = [
                room
                for room in self.spaceship.rooms
                if room.pos[0] <= pos[0] and pos[0] <= room.pos[0] + 100
                and room.pos[1] <= pos[1] and pos[1] <= room.pos[1] + 100
            ]
            if hovered_room:
                hovered_room[0].add_crew_member(grabbed_crew_member[0])
            else:
                hq_room = [room for room in self.spaceship.rooms if room.type == "HQ"][0]
                hq_room.add_crew_member(grabbed_crew_member[0])
        else:
            crew_member = [
                member
                for member in self.spaceship.crew
                if member.pos[0] <= pos[0] + 8 and pos[0] <= member.pos[0] + 24
                and member.pos[1] <= pos[1] + 8 and pos[1] <= member.pos[1] + 24
            ]

            if crew_member:
                if not crew_member[0].current_room:
                    return
                crew_member[0].grabbed = True
                crew_member[0].current_room.remove_crew_member(crew_member[0])

    def __repr__(self):
        return "Spaceship: {}\n".format(self.spaceship)


def createCrew():
    res_folder = ulis43.basedir / "res"
    randnames_file = res_folder / "crew_names.yaml"
    with randnames_file.open() as f:
        randnames = yaml.safe_load(f)
    game_strings_file = res_folder / "strings.yaml"
    with game_strings_file.open() as f:
        game_strings = yaml.safe_load(f)
    skills = game_strings["SKILLS"]
    shapes = game_strings["SHAPE"]
    res_types = game_strings["RESSOURCES"]


    # skills

    crewmember_skills = dict.fromkeys(skills, 0)
    skill2distrib = list(skills)
    random.shuffle(skill2distrib)

    total_points = random.randint(50, 200)
    dominant = skills[random.randint(0, len(skills) - 1)]

    crewmember_skills[dominant] = min(total_points * random.uniform(0.25, 0.8), 100)
    skill2distrib.remove(dominant)
    total_points = max(0, total_points - crewmember_skills[dominant])

    for skill in skill2distrib:
        if len(skill2distrib) > 1:
            crewmember_skills[skill] = min(total_points * random.random(), 100)
            total_points = max(0, total_points - crewmember_skills[skill])
            skill2distrib.remove(skill)
        else:
            crewmember_skills[skill] = total_points

    # stats

    stats = dict.fromkeys(res_types, 100)
    stats["hp"] = 100
    stats["shape"] = shapes[random.randint(0, len(shapes) - 1)]
    stats["velocity"] = 1.0  # m/s

    # consumption

    consumption = dict.fromkeys(res_types, 1)
    if stats["shape"] == "BIG":
        consumption["FOOD"] *= 2
        stats["velocity"] *= 0.75
    if stats["shape"] == "MUSCULAR":
        consumption["WATER"] *= 2
        consumption["FOOD"] *= 1.5
        stats["velocity"] *= 1.5

    return ulis43.crew_member.CrewMember(
        name=randnames[random.randint(0, len(randnames) - 1)],
        skills=crewmember_skills,
        state="NOMINAL",
        stats=stats,
        consumption=consumption
    )
