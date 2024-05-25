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

        '''

        # Here is where we draw the background with a base grass tile, it leaves a one tile border around each side
        for col in range(43):
            for row in range(26):
                self.tilemap[str(col + 1) + ';' + str(row + 1)] = {'type': 'grass', 'variant': 1, 'pos': (col + 1, row + 1)}

        # Here we draw a platform for our base to rest on
        for col in range(3):
            for row in range(3):
                self.tilemap[str(40 + col) + ';' + str(2 + row)] = {'type': 'dirt', 'variant': 1, 'pos': (40 + col, 2 + row)}

        # Here we draw pathways for the monster to travel towards our base
        for col in range(10):
            self.tilemap[str(1 + col) + ';' + str(24)] = {'type': 'dirt', 'variant': 1, 'pos': (1 + col, 24)}

        for row in range(10):
            self.tilemap['10;' + str(14 + row)] = {'type': 'dirt', 'variant': 1, 'pos': (10, 14 + row)}

        for col in range(8):
            self.tilemap[str(11 + col) + ';14'] = {'type': 'dirt', 'variant': 1, 'pos': (11 + col, 14)}

        for row in range(10):
            self.tilemap['19;' + str(14 + row)] = {'type': 'dirt', 'variant': 1, 'pos': (19, 14 + row)}

        for col in range(20):
            self.tilemap[str(19 + col) + ';' + str(24)] = {'type': 'dirt', 'variant': 1, 'pos': (19 + col, 24)}

        for row in range(15):
            self.tilemap['39;' + str(10 + row)] = {'type': 'dirt', 'variant': 1, 'pos': (39, 10 + row)}

        for col in range(8):
            self.tilemap[str(31 + col) + ';' + str(10)] = {'type': 'dirt', 'variant': 1, 'pos': (31 + col, 10)}

        for row in range(8):
            self.tilemap['31;' + str(10 + row)] = {'type': 'dirt', 'variant': 1, 'pos': (31, 10 + row)}

        for col in range(8):
            self.tilemap[str(24 + col) + ';' + str(18)] = {'type': 'dirt', 'variant': 1, 'pos': (24 + col, 18)}

        for row in range(15):
            self.tilemap['24;' + str(3 + row)] = {'type': 'dirt', 'variant': 1, 'pos': (24, 3 + row)}

        for col in range(15):
            self.tilemap[str(25 + col) + ';' + str(3)] = {'type': 'dirt', 'variant': 1, 'pos': (25 + col, 3)}
        '''

    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0], tile['pos'][1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
