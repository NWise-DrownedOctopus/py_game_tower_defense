import pygame
import sys
import json
from scripts.utils import load_image, load_images, draw_text
from scripts import level, ui
import main

FPS = 60

class Map:
    def __init__(self):
        self.game = None
        self.levels = None
        self.bg_color = (25, 25, 25)
        self.clock = pygame.time.Clock()
        self.render_scale = 2.0

        self.assets = {'mouse_pointer': load_image("mouse_pointer.png")}

        pygame.init()
        pygame.display.set_caption("tower defense game")

        self.screen = pygame.display.set_mode(
            (1280, 720))

        self.screen_mpos = None
        self.text_font = pygame.font.SysFont("arial", 20)

        self.display = pygame.Surface((640, 360))
        self.dt = 0

        self.selected_level = None
        self.game_ui = ui.UI("ow_map")

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.levels = map_data['levels']

    def run(self):
        # here is where we initialize the game, before our while loop, this code only runs once
        pygame.mouse.set_visible(False)

        self.load('data/overworld_map.json')

        self.game_ui.create_over_world_buttons()

        print("We Finished Start in map")

        while True:
            # Here is where we can draw our background
            self.screen.fill(self.bg_color)
            self.display.fill(self.bg_color)

            # here is where we manage the mouse position input
            self.screen_mpos = pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1] / 2

            # Here we display our UI
            for button in self.game_ui.buttons:
                button.draw_button(self.display)

            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.game_ui.check_click() == 'l1':
                            self.selected_level = '1'
                        if self.game_ui.check_click() == 'l2':
                            self.selected_level = '2'
                        if self.game_ui.check_click() == 'l3':
                            self.selected_level = '3'
                        if self.game_ui.check_click() == 'play' and self.selected_level is not None:
                            print("We tried to enter level")
                            self.game = main.Game()
                            self.game.current_level = self.levels[self.selected_level][0]
                            self.game.run()

            # Here we display our mouse
            self.display.blit(self.assets['mouse_pointer'], self.screen_mpos)

            self.screen.blit(pygame.transform.scale(self.display, (1280, 720)), (0, 8))

            draw_text(self.screen, 'Level 1', self.text_font, (255, 255, 255), 200, 185)
            draw_text(self.screen, 'Level 2', self.text_font, (255, 255, 255), 400, 385)
            draw_text(self.screen, 'Level 3', self.text_font, (255, 255, 255), 300, 285)

            pygame.display.update()
            self.dt = self.clock.tick(FPS) / 1000

