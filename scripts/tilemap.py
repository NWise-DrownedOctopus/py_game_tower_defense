import json

class Tilemap:
    """
    Our current working screen resolution is going to be set at 2880 x 1800
    however, we are scaling up a display resolution of  1440, 900 to get there

    if our tiles are 16 x 16 pixels but doubled to 32 x 32 pixels:
    Our max Width is 45 tiles (1440 pixels)
    Our max Height is 28.125 tiles tall (900 pixels)
    if we do only 28 tiles we have 2 extra pixels
    """

    def __init__(self, game, tile_size=16):
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
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
