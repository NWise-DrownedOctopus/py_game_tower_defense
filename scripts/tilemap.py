import json


class Tilemap:
    """
    Our target is to have 16 x 16 tiles, that scale up x2 to be 32 x 32
    Our map is going to have a limit of 51 x 33 tiles to make sure the map fits on any monitor we want to support,
    and so that we have plenty of room for UI on the sides of the screen
    """

    def __init__(self, game, tile_size):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def save(self, path):
        print('We called save function')
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        print(f)
        f.close()
        print(f)

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0], tile['pos'][1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']],
                      (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

    def get_tile(self, pos):
        try:
            tile = self.tilemap[str(pos[0]) + ';' + str(pos[1])]
        except KeyError:
            return None
        return tile
