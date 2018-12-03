import yaml
import random
import ulis43
import ulis43.rooms
import ulis43.spaceship
import ulis43.crew_member


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

        print(min_x, max_x)
        print(min_y, max_y)
        print(center_x, center_y)
        print(delta_x, delta_y)

        positions = [(p[0] * 100 - delta_x, p[1] * 100 - delta_y) for p in positions]

        for i, room in enumerate(rooms):
            room.pos = positions[i]

        # Crew

        randnames_file = res_folder / "crew_names.yaml"
        with randnames_file.open() as f:
            randnames = yaml.safe_load(f)
        game_strings_file = res_folder / "strings.yaml"
        with game_strings_file.open() as f:
            game_strings = yaml.safe_load(f)
        skills = game_strings["SKILLS"]
        shapes = game_strings["SHAPE"]
        res_types = game_strings["RESSOURCES"]

        crew = []
        for _ in range(ship_config["crew_size"]):

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

            crew.append(ulis43.crew_member.CrewMember(
                name=randnames[random.randint(0, len(randnames) - 1)],
                skills=crewmember_skills,
                state="NOMINAL",
                stats=stats,
                consumption=consumption
            ))

            randroom = random.sample(rooms, 1)[0]
            randroom.add_crew_member(crew[-1])

        # Instanciate spaceship

        self.spaceship = ulis43.spaceship.Spaceship(
            ressources=ressources,
            crew=crew,
            rooms=rooms
        )

    def tick(self):
        self.spaceship.tick()

    def draw(self, ctx):
        self.spaceship.draw(ctx)

    def __repr__(self):
        return "Spaceship: {}\n".format(self.spaceship)
