import yaml
import ulis43


class Game:

    def __init__(self):
        strings_file = ulis43.basedir / "res" / "strings.yaml"
        with strings_file.open() as f:
            strings = yaml.safe_load(f)
        self.strings = strings
