import yaml
import ulis43
import ulis43.rooms
import ulis43.spaceship


class Game:

    def __init__(self, difficulty="easy"):

        res_folder = ulis43.basedir / "res"
        config_file = res_folder / "config.yaml"

        with config_file.open() as f:
            config = yaml.safe_load(f)
        self.config = config

        ship_config = config["difficulty"][difficulty]
        ressources = ship_config['ressources']
        # todo: see how to autoload python classes with yaml correctly
        # !!python/object:ulis43.rooms.Room didn't work
        rooms = []
        for room in ship_config['rooms']:
            rooms.append(ulis43.rooms.Room(**room))

        self.spaceship = ulis43.spaceship.Spaceship(
            ressources=ressources,
            crew=None,
            rooms=rooms
        )
