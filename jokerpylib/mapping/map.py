

import json
class Map:

    _map: dict

    @staticmethod
    def load_json(abspath: str):
        with open(abspath,"r") as fp:
            Map._map = json.load(fp)

    @staticmethod
    def get_map():
        return Map._map