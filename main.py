import sys
import os

import pygame

from scripts import tower
from scripts import monster
from scripts import gem
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

        self.bg_color = (25, 25, 25)

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode(
            (pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]))

        self.display = pygame.Surface((640, 360))

        self.clock = pygame.time.Clock()

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

        self.build_mode = False
        self.paused = True
        self.pathfinding_mode = False
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.mpos = None
        self.screen_mpos = pygame.mouse.get_pos()

        # here is where we initialize our tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        self.pathfinding = Pathfinding(self)
        self.game_ui = ui.UI(self)
        self.pf_grid = make_grid(ROWS, WIDTH)
        self.pf_started = False
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

    def run(self):
        # here is where we initialize the game, before our while loop, this code only runs once
        pygame.mouse.set_visible(False)

        # Here is where we can initialize the scene
        towers = pygame.sprite.Group()
        gems = pygame.sprite.Group()
        monsters = pygame.sprite.Group()
        self.game_ui.create_buttons()
        monster_spawn_pos = self.pf_grid[6][22].row, self.pf_grid[6][22].col

        # Here we will initialize 16 x 9 ratios (My PC)
        if self.screen.get_size()[0] == 2560 and self.screen.get_size()[1] == 1440:
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 16))
            self.render_scale = 4.0
        # Here we will initialize 16 x 10 ratios (My Laptop)
        if self.screen.get_size()[0] == 2880 and self.screen.get_size()[1] == 1800:
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.render_scale = 3.0
        if self.screen.get_size()[0] == 1440 and self.screen.get_size()[1] == 900:
            self.screen.blit(pygame.transform.scale(self.display, (1280, 720)), (0, 90))
            self.render_scale = 2.0

        # Here is where we initialize our dynamic elements
        monster1 = monster.Monster(monster_spawn_pos[0], monster_spawn_pos[1], self.pathfinding, self.render_scale,)
        monsters.add(monster1)

        # pf_start, pf_end = self.start()
        # here we manage pathfinding initialization
        pf_start = self.pf_grid[6][21]
        pf_start.make_start()
        pf_end = self.pf_grid[29][4]
        pf_end.make_end()
        pf_started = True
        print("We Finished Start")
        '''
        if len(monsters) >= 1:
            monsters.sprites()[0].find_path()
        '''

        # Here we enter the game loop, it is called "every frame"
        while True:
            # Here is where we can draw our background
            self.screen.fill(self.bg_color)
            self.display.fill(self.bg_color)
            self.tilemap.render(self.display)

            # here is where we manage the mouse position input
            self.screen_mpos = pygame.mouse.get_pos()

            # This feels super hacky, and I think I should attempt to refactor this to be more elegant
            if self.screen.get_size()[0] == 1440 and self.screen.get_size()[1] == 900:
                self.mpos = ((self.screen_mpos[0] / self.render_scale), (self.screen_mpos[1] / self.render_scale) - 45)
                tile_pos = (int(self.mpos[0] // self.tilemap.tile_size), int(self.mpos[1] // self.tilemap.tile_size))
                if tile_pos[0] <= 1:
                    tile_pos = (2, tile_pos[1])
                if tile_pos[0] >= 33:
                    tile_pos = (33, tile_pos[1])
                if tile_pos[1] <= 0:
                    tile_pos = (tile_pos[0], 0)
                if tile_pos[1] >= 21:
                    tile_pos = (tile_pos[0], 21)

            # Here is where we manage pathfinding
            if self.pathfinding_mode:
                self.display.blit(self.assets['pathfinding_indicator'], (600, 20))
                self.pathfinding.update()

            # here is where we handle build mode
            if self.build_mode:
                self.display.blit(self.assets['build_indicator'], (600, 320))
                current_building = self.assets['tower'].copy()
                current_building.set_alpha(100)
                self.display.blit(current_building, (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size))

            # Here is where we draw our static elements to the screen
            for player_tower in towers:
                player_tower.draw()
            for player_gem in gems:
                player_gem.draw()

            # Here is where we make our monsters move
            for enemy_monster in monsters:
                enemy_monster.draw(self.display)
                enemy_monster.update()

            # Here is where we check if the monster is in range of the turret
            for p_tower in towers:
                if monsters is not None:
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

                if self.pf_started:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if self.build_mode:
                            if self.clicking:
                                tower_n = tower.Tower(
                                    (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size),
                                    self.display)
                                towers.add(tower_n)
                        else:
                            if self.game_ui.check_click() == 'play':
                                print("we would like to play")
                                # self.paused = False
                                self.pathfinding.update()
                                row = tile_pos[0]
                                col = tile_pos[1]
                                tile = self.pf_grid[row][col]
                                if not pf_start and tile != pf_end:
                                    pf_start = tile
                                    pf_start.make_start()
                                elif not pf_end and tile != pf_start:
                                    pf_end = tile
                                    pf_end.make_end()
                                elif tile != pf_end and tile != pf_start:
                                    tile.make_barrier()
                                if not self.pf_started and self.paused:
                                    self.paused = False
                                    for row in self.pf_grid:
                                        for tile in row:
                                            tile.update_neighbors(self.pf_grid)

                                    pf_algorithm(lambda: draw_pathfinding(self.display, self.pf_grid, ROWS, WIDTH),
                                                 self.pf_grid, pf_start, pf_end, self)
                                    if len(monsters) >= 1:
                                        monsters.sprites()[0].find_path()

                            if self.game_ui.check_click() == 'pause':
                                print("we would like to pause")
                                self.paused = True
                            if self.game_ui.check_click() == 'fast_forward':
                                print("we would like to fast_forward")

                        if self.pathfinding_mode:
                            row = tile_pos[0]
                            col = tile_pos[1]
                            tile = self.pf_grid[row][col]
                            if not pf_start and tile != pf_end:
                                pf_start = tile
                                pf_start.make_start()
                            elif not pf_end and tile != pf_start:
                                pf_end = tile
                                pf_end.make_end()
                            elif tile != pf_end and tile != pf_start:
                                tile.make_barrier()

                    if event.button == 3:
                        self.right_clicking = True
                        if self.pathfinding_mode:
                            row = tile_pos[0]
                            col = tile_pos[1]
                            tile = self.pf_grid[row][col]
                            tile.reset()
                            if tile == pf_start:
                                pf_start = None
                            if tile == pf_end:
                                pf_end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.build_mode = not self.build_mode
                    if event.key == pygame.K_p:
                        self.pathfinding_mode = not self.pathfinding_mode
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused

            # Here we handle UI input

            # Here we start the loop by drawing the background of the scene first
            # This layout is for our laptop
            # We currently have 33 x 22 tiles?
            # We are scaling up by two at this resolution, and tiles were designed at 16x16 pixels (32x32 once scaled)
            # this means our play area is taking up 1280 x 720
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
                self.render_scale = 4.0

            # Here we display our mouse
            self.screen.blit(self.assets['mouse_pointer'], self.screen_mpos)

            pygame.display.update()
            self.clock.tick(FPS)


Game().run()
