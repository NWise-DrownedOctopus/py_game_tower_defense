import sys
import os

import pygame

from scripts import tower
from scripts import monster
from scripts import ui
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap
from pathfinding import Pathfinding, make_grid, draw_pathfinding
from pathfinding import algorithm as pf_algorithm

FPS = 60
WIDTH = 640
ROWS = 40


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("tower defense game")

        self.screen = pygame.display.set_mode(
            (pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]))

        self.display = pygame.Surface((640, 360))

        # here we will import all the assets we need in our game at runtime
        self.assets = {
            'player': load_image("player.png"),
            'grass': load_images("grass"),
            'dirt': load_images("dirt"),
            'build_indicator': load_image("build_indicator.png"),
            'pathfinding_indicator': load_image("pathfinding_indicator.png"),
            'mouse_pointer': load_image("mouse_pointer.png"),
            'tower': load_image("tower.png"),
            'l_side_bar': load_image("UI_L_SideBar.png"),
            'r_side_bar': load_image("UI_R_SideBar.png"),
            'top_bar': load_image("UI_TopBar.png"),
            'bottom_bar': load_image("UI_BottomBar.png"),
            'play_button': load_image("play_button.png"),
            'pause_button': load_image("pause_button.png"),
            'fast_forward_button': load_image("fast_forward_button.png")
        }

        self.clock = pygame.time.Clock()
        self.bg_color = (25, 25, 25)
        self.build_mode = False
        self.paused = True
        self.pathfinding_mode = False
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.mpos = None
        self.screen_mpos = pygame.mouse.get_pos()
        self.tile_pos = None
        self.debug_mode = False

        # Here is where we can initialize the scene
        self.towers = pygame.sprite.Group()
        self.gems = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        # here is where we initialize our tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        self.pathfinding = Pathfinding(self)
        self.game_ui = ui.UI(self)
        self.pf_grid = make_grid(ROWS, WIDTH)
        self.pf_started = False
        # here we manage pathfinding initialization
        self.pf_start = self.pf_grid[6][21]
        self.pf_start.make_start()
        self.pf_end = self.pf_grid[29][4]
        self.pf_end.make_end()
        filepath = r"data"
        self.render_scale = 1.0
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

    def init_resolution(self):
        # Here we will initialize 16 x 9 ratios (My PC)
        if self.screen.get_size()[0] == 2560 and self.screen.get_size()[1] == 1440:
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 16))
            self.render_scale = 4.0
        # Here we will initialize 16 x 10 ratios (My Laptop)
        elif self.screen.get_size()[0] == 2880 and self.screen.get_size()[1] == 1800:
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.render_scale = 3.0
        elif self.screen.get_size()[0] == 1440 and self.screen.get_size()[1] == 900:
            self.screen.blit(pygame.transform.scale(self.display, (1280, 720)), (0, 90))
            self.render_scale = 2.0
        else:
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

    def run_pathfinding(self):
        if self.game_ui.check_click() == 'play':
            print("we would like to play")
            if self.debug_mode:
                self.pathfinding.update(True)
            else:
                self.pathfinding.update()
            row = self.tile_pos[0]
            col = self.tile_pos[1]
            tile = self.pf_grid[row][col]
            if not self.pf_start and tile != self.pf_end:
                pf_start = tile
                pf_start.make_start()
            elif not self.pf_end and tile != self.pf_start:
                pf_end = tile
                pf_end.make_end()
            elif tile != self.pf_end and tile != self.pf_start:
                tile.make_barrier()
            if not self.pf_started and self.paused:
                self.paused = False
                for row in self.pf_grid:
                    for tile in row:
                        tile.update_neighbors(self.pf_grid)
                if self.debug_mode:
                    pf_algorithm(lambda: draw_pathfinding(self.display, self.pf_grid, ROWS, WIDTH),
                                 self.pf_grid, self.pf_start, self.pf_end, self, True)
                else:
                    pf_algorithm(lambda: draw_pathfinding(self.display, self.pf_grid, ROWS, WIDTH),
                                 self.pf_grid, self.pf_start, self.pf_end, self)
                if len(self.monsters) >= 1:
                    self.monsters.sprites()[0].find_path()

    def run(self):
        # here is where we initialize the game, before our while loop, this code only runs once
        pygame.mouse.set_visible(False)

        self.game_ui.create_buttons()
        self.init_resolution()

        # Here is where we initialize our dynamic elements
        monster_spawn_pos = self.pf_grid[6][22].row, self.pf_grid[6][22].col
        monster1 = monster.Monster(monster_spawn_pos[0], monster_spawn_pos[1], self.pathfinding, self.render_scale,)
        self.monsters.add(monster1)

        print("We Finished Start")

        # Here we enter the game loop, it is called "every frame"
        while True:
            # Here is where we can draw our background
            self.screen.fill(self.bg_color)
            self.display.fill(self.bg_color)
            self.tilemap.render(self.display)

            # here is where we manage the mouse position input
            self.screen_mpos = pygame.mouse.get_pos()

            # This feels super hacky, and I think I should attempt to refactor this to be more elegant
            # This is our solution for my laptop
            self.tile_pos = self.mpos
            if self.screen.get_size()[0] == 1440 and self.screen.get_size()[1] == 900:
                self.mpos = ((self.screen_mpos[0] / self.render_scale), (self.screen_mpos[1] / self.render_scale) - 45)
                self.tile_pos = (int(self.mpos[0] // self.tilemap.tile_size), int(self.mpos[1] // self.tilemap.tile_size))
            # This is my solution for my pc
            if self.screen.get_size()[0] == 2560 and self.screen.get_size()[1] == 1440:
                self.mpos = ((self.screen_mpos[0] / self.render_scale), (self.screen_mpos[1] / self.render_scale))
                self.tile_pos = (int(self.mpos[0] // self.tilemap.tile_size), int(self.mpos[1] // self.tilemap.tile_size))

            # Here we are making sure our tile_position doesn't go out of bounds of the current game display area
            if self.tile_pos[0] <= 0:
                self.tile_pos = (1, self.tile_pos[1])
            if self.tile_pos[0] >= 33:
                self.tile_pos = (33, self.tile_pos[1])
            if self.tile_pos[1] <= 0:
                self.tile_pos = (self.tile_pos[0], 0)
            if self.tile_pos[1] >= 21:
                self.tile_pos = (self.tile_pos[0], 21)

            # Here is where we manage pathfinding
            if self.debug_mode:
                self.display.blit(self.assets['pathfinding_indicator'], (600, 20))
                self.pathfinding.update(True)

            # here is where we handle build mode
            if self.build_mode:
                self.display.blit(self.assets['build_indicator'], (600, 320))
                current_building = self.assets['tower'].copy()
                current_building.set_alpha(100)
                self.display.blit(current_building, (self.tile_pos[0] * self.tilemap.tile_size, self.tile_pos[1] * self.tilemap.tile_size))

            # Here is where we draw our static elements to the screen
            for player_tower in self.towers:
                player_tower.draw()
            for player_gem in self.gems:
                player_gem.draw()

            # Here is where we make our monsters move
            for enemy_monster in self.monsters:
                enemy_monster.draw(self.display)
                enemy_monster.update()

            # Here is where we check if the monster is in range of the turret
            for p_tower in self.towers:
                if self.monsters is not None:
                    for e_monster in self.monsters:
                        p_tower.detect_monster(e_monster)
            for p_gem in self.gems:
                p_gem.update()

            # Here we update our projectiles
            for player_gem in self.gems:
                for projectile in player_gem.projectiles:
                    projectile.update()

            # This is the event checker for each frame
            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.pf_started:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if self.build_mode:
                            if self.clicking:
                                tower_n = tower.Tower(
                                    (self.tile_pos[0] * self.tilemap.tile_size, self.tile_pos[1] * self.tilemap.tile_size),
                                    self.display)
                                self.towers.add(tower_n)
                        else:
                            if self.game_ui.check_click() == 'play':
                                self.run_pathfinding()
                            if self.game_ui.check_click() == 'pause':
                                print("we would like to pause")
                                self.paused = True
                            if self.game_ui.check_click() == 'fast_forward':
                                print("we would like to fast_forward")

                        if self.debug_mode:
                            row = self.tile_pos[0]
                            col = self.tile_pos[1]
                            tile = self.pf_grid[row][col]
                            if not self.pf_start and tile != self.pf_end:
                                pf_start = tile
                                pf_start.make_start()
                            elif not self.pf_end and tile != self.pf_start:
                                pf_end = tile
                                pf_end.make_end()
                            elif tile != self.pf_end and tile != self.pf_start:
                                tile.make_barrier()

                    if event.button == 3:
                        self.right_clicking = True
                        if self.debug_mode:
                            row = self.tile_pos[0]
                            col = self.tile_pos[1]
                            tile = self.pf_grid[row][col]
                            tile.reset()
                            if tile == self.pf_start:
                                self.pf_start = None
                            if tile == self.pf_end:
                                self.pf_end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.build_mode = not self.build_mode
                    if event.key == pygame.K_p:
                        self.debug_mode = not self.debug_mode
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused

            # Here we handle UI input

            # Here we start the loop by drawing the background of the scene first
            if self.screen.get_size()[0] == 1440 and self.screen.get_size()[1] == 900:
                self.screen.blit(pygame.transform.scale(self.display, (1280, 720)), (0, 90))
                # Left bar at this resolution should be at (0, 0) with the dim. (32 x 1440)
                # self.screen.blit(self.assets['l_side_bar'], (0, 0))
                pygame.draw.rect(self.screen, (245, 190, 37), pygame.Rect(0, 0, 32, 1440))

                # Right bar at this resolution should be at (1088, 0) with the dim. (128 x 1440)
                pygame.draw.rect(self.screen, (245, 190, 37), pygame.Rect(1088, 0, 352, 1440))
                # self.screen.blit(self.assets['r_side_bar'], (1088, 0))

                # Top bar at this resolution should be at (32, 0) with the dim. (1056 x 80)
                pygame.draw.rect(self.screen, (200, 150, 10), pygame.Rect(32, 0, 1056, 90))
                # self.screen.blit(self.assets['top_bar'], (64, 0))

                # Bottom bar at this resolution should be at (32, 810) with the dim. (1056 x 90)
                # However our tile grid is slightly too tall because we have an extra half tile in height
                # that adds an extra 16 pixels for us here
                pygame.draw.rect(self.screen, (200, 150, 10), pygame.Rect(32, 794, 1056, 106))
                # self.screen.blit(self.assets['bottom_bar'], (64, 794))

                for button in self.game_ui.buttons:
                    button.draw_button()

                self.render_scale = 2.0

            if self.screen.get_size()[0] == 2560 and self.screen.get_size()[1] == 1440:
                self.screen.blit(pygame.transform.scale(self.display, (2560, 1440)), (0, 16))
                # Left bar at this resolution should be at (0, 0) with the dim. (32 x 1440)
                # self.screen.blit(self.assets['l_side_bar'], (0, 0))
                pygame.draw.rect(self.screen, (245, 190, 37), pygame.Rect(0, 0, 64, 1440))

                # Right bar at this resolution should be at (1088, 0) with the dim. (128 x 1440)
                pygame.draw.rect(self.screen, (245, 190, 37), pygame.Rect(2176, 0, 384, 1440))
                # self.screen.blit(self.assets['r_side_bar'], (1088, 0))

                # Top bar at this resolution should be at (32, 0) with the dim. (1056 x 80)
                pygame.draw.rect(self.screen, (200, 150, 10), pygame.Rect(64, 0, 2112, 16))
                # self.screen.blit(self.assets['top_bar'], (64, 0))

                # Bottom bar at this resolution should be at (32, 810) with the dim. (1056 x 90)
                # However our tile grid is slightly too tall because we have an extra half tile in height
                # that adds an extra 16 pixels for us here
                pygame.draw.rect(self.screen, (200, 150, 10), pygame.Rect(64, 1424, 2112, 16))
                # self.screen.blit(self.assets['bottom_bar'], (64, 794))

                for button in self.game_ui.buttons:
                    button.draw_button()
                self.render_scale = 4.0

            # Here we display our mouse
            self.screen.blit(self.assets['mouse_pointer'], self.screen_mpos)

            pygame.display.update()
            self.clock.tick(FPS)


Game().run()
