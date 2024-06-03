import os
import sys

import pygame

from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

FPS = 60

RENDER_SCALE = 4


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("editor")

        self.SCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][0]
        self.SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0][1]
        print(pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1])

        self.bg_color = (25, 25, 25)

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode(
            (pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]))

        # Here we will initialize 16 x 9 ratios (My PC)
        if self.screen.get_size()[0] == 2560 and self.screen.get_size()[1] == 1440:
            self.display = pygame.Surface((640, 360))

        # Here we will initialize 16 x 10 ratios (My Laptop)
        if self.screen.get_size()[0] == 1440 and self.screen.get_size()[1] == 900:
            self.display = pygame.Surface((640, 360))

        self.clock = pygame.time.Clock()

        self.tile_size = 16

        # here we will import all the assets we need in our game at runtime
        self.assets = {
            'grass': load_images("grass"),
            'dirt': load_images("dirt")
        }

        # here is where we initialize our tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        filepath = r"data"
        try:
            if os.path.exists(filepath):
                print('loaded tilemap successfully')
                self.tilemap.load("data/map.json")
            else:
                print("File not found: " + filepath)
        except FileNotFoundError:
            print("File not found: " + filepath)
        except PermissionError:
            print("Did not have permission to load file")

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.on_grid = True

    def run(self):
        # Here we enter the game loop, it is called "every frame"
        while True:
            # Here is where we can draw our background
            self.display.fill(self.bg_color)

            self.tilemap.render(self.display)

            current_tile = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int(mpos[0] // self.tilemap.tile_size), int(mpos[1] // self.tilemap.tile_size))

            # here we will preview our tile placement
            if self.on_grid:
                self.display.blit(current_tile, (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size))
            else:
                self.display.blit(current_tile, mpos)

            # here we will add tiles to our tilemap if the player clicks the mouse button
            # The selection is based on our currently selected tile
            if self.clicking and self.on_grid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0], tile['pos'][1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile, (5, 5))

            # This is the event checker for each frame
            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        # here is where we place a tile if grid snap is turned off
                        if not self.on_grid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': mpos})

                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            pass
                        if event.button == 5:
                            pass
                    else:
                        if event.button == 4:
                            pass
                        if event.button == 5:
                            pass
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid
                    if event.key == pygame.K_o:
                        print('We Hit o')
                        self.tilemap.save('data/map.json')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        print("left up")
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    if event.key == pygame.K_RIGHT:
                        print("right up")
                        self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                    if event.key == pygame.K_UP:
                        print("Up up")
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.key == pygame.K_DOWN:
                        print("Down up")
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(FPS)


Editor().run()
