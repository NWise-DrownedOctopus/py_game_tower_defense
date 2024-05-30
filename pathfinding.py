from scripts.tilemap import Tilemap
import os

class PathFinding:
    def __init__(self):
        # here is where we initialize our tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        filepath = r"C:\Users\nicho\PycharmProjects\py_game_tower_defense\data"
        try:
            if os.path.exists(filepath):
                print('loaded tilemap successfully')
                self.tilemap.load("C:/Users/nicho/PycharmProjects/py_game_tower_defense/data/map.json")
            else:
                print("File not found: " + filepath)
        except FileNotFoundError:
            print("File not found: " + filepath)
        except PermissionError:
            print("Did not have permission to load file")
