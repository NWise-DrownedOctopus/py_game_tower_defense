import json

class Tilemap:

    def __init__(self, game, tile_size):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def save(self, path):
        try:
            with open(path, 'w') as f:
                json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        except PermissionError:
            print(f"Permission denied when saving tilemap to {path}")
        except OSError as e:
            print(f"Failed to save tilemap: {e}")

    def load(self, path):
        try:
            with open(path, 'r') as f:
                map_data = json.load(f)
            self.tilemap = map_data['tilemap']
            self.tile_size = map_data['tile_size']
            self.offgrid_tiles = map_data['offgrid']
        except FileNotFoundError:
            print(f"Tilemap file not found: {path}")
        except PermissionError:
            print(f"Permission denied when loading tilemap: {path}")
        except json.JSONDecodeError as e:
            print(f"Tilemap file is malformed: {e}")

    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0], tile['pos'][1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']],
                      (tile['pos'][0] * self.tile_size * 2, tile['pos'][1] * self.tile_size * self.game.render_scale))

    def get_tile(self, pos):
        try:
            tile = self.tilemap[f"{pos[0]};{pos[1]}"]
        except KeyError:
            return None
        return tile
