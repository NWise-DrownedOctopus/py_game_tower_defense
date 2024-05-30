import sys
import os

import pygame

from scripts import tower
from scripts import monster
from scripts import gem
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

# monster details
monster_pos = [626, 222]
monster_movement = [False, False]
monster_v_movement = [False, False]

FPS = 60
RENDER_SCALE = 1.0


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("tower defense game")

        self.SCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][0]
        self.SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0][1]

        self.bg_color = (25, 25, 25)

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode((2880, 1800))

        self.display = pygame.Surface((1440, 900))

        self.clock = pygame.time.Clock()

        # here we will import all the assets we need in our game at runtime
        self.assets = {
            'player': load_image("player.png"),
            'grass': load_images("grass"),
            'dirt': load_images("dirt"),
            'build_indicator': load_image("build_indicator.png"),
            'mouse_pointer': load_image("mouse_pointer.png"),
            'tower': load_image("tower.png")
        }

        self.build_mode = False
        self.clicking = False
        self.right_clicking = False

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

    def run(self):
        # here is where we initialize the game, before our while loop, this code only runs once
        pygame.mouse.set_visible(False)
        # Here is where we can initialize the scene
        towers = pygame.sprite.Group()
        gems = pygame.sprite.Group()
        monsters = pygame.sprite.Group()

        # Here is where we initialize all of our static elements in the scene
        # I put them in relevant lists, so that they can be updated in batches
        tower1 = tower.Tower([226, 222], self.screen)
        towers.add(tower1)
        gem1 = gem.Gem([226, 222], self.screen, tower1)
        gems.add(gem1)

        # Here is where we initialize our dynamic elements
        monster1 = monster.Monster(monster_pos[0], monster_pos[1])
        monsters.add(monster1)

        # Here we enter the game loop, it is called "every frame"
        while True:
            # Here is where we can draw our background
            self.display.fill(self.bg_color)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.tilemap.render(self.display)

            # here is where we manage the mouse position input
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int(mpos[0] // self.tilemap.tile_size), int(mpos[1] // self.tilemap.tile_size))
            self.screen.blit(self.assets['mouse_pointer'], mpos)

            # here is where we handle build mode
            if self.build_mode:
                self.screen.blit(self.assets['build_indicator'], (5, 5))
                current_building = self.assets['tower'].copy()
                current_building.set_alpha(100)
                self.screen.blit(current_building, (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size))


            # Here is where we draw our static elements to the screen
            for player_tower in towers:
                player_tower.draw()
            for player_gem in gems:
                player_gem.draw()

            # Here is where we update the position of the monster
            monster1.draw(self.screen, monster_pos)
            monster_pos[0] += (monster_movement[1] - monster_movement[0]) * monster1.monster_move_speed
            monster_pos[1] += (monster_v_movement[1] - monster_v_movement[0]) * monster1.monster_move_speed

            # Here is where we check if the monster is in range of the turret
            for p_tower in towers:
                for e_monster in monsters:
                    p_tower.detect_monster(e_monster)
            for p_gem in gems:
                p_gem.update()

            # Here we update our projectiles
            for player_gem in gems:
                for projectile in player_gem.projectiles:
                    projectile.update()

            # This is the event checker for each frame
            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if self.build_mode:
                            if self.clicking:
                                tower_n = tower.Tower(
                                    (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size),
                                    self.screen)
                                towers.add(tower_n)
                    if event.button == 3:
                        self.right_clicking = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        monster_movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        monster_movement[1] = True
                    if event.key == pygame.K_UP:
                        monster_v_movement[0] = True
                    if event.key == pygame.K_DOWN:
                        monster_v_movement[1] = True
                    if event.key == pygame.K_b:
                        self.build_mode = not self.build_mode
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        monster_movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        monster_movement[1] = False
                    if event.key == pygame.K_UP:
                        monster_v_movement[0] = False
                    if event.key == pygame.K_DOWN:
                        monster_v_movement[1] = False
                        # Here we start the loop by drawing the background of the scene first

            pygame.display.update()
            self.clock.tick(FPS)


Game().run()
