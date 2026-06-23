import pygame
import sys
import json
from scripts.utils import draw_text
from scripts import ui
import main

FPS = 60

class Map:
    def __init__(self, save_data=None):
        self.game = None
        self.levels = None
        self.bg_color = (25, 25, 25)
        self.clock = pygame.time.Clock()
        self.render_scale = 2.0
        self.save_data = save_data
        self.map_ended = False

        pygame.display.set_caption("Errour: Canto")

        self.screen = pygame.display.set_mode(
            (1280, 720))

        self.screen_mpos = None
        self.text_font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 20)

        self.display = pygame.Surface((640, 360))
        self.dt = 0

        self.selected_level = None
        self.game_ui = ui.UI("ow_map")

    def load(self, path):
        with open(path, 'r') as f:
            map_data = json.load(f)
        self.levels = map_data['levels']

    def run(self):
        # here is where we initialize the game, before our while loop, this code only runs once
        pygame.mouse.set_visible(False)

        self.load('data/overworld_map.json')

        l1_button = ui.Button(self.game_ui, 32, 32, (300, 100), 'l1', self.game_ui.assets["mars_hex_01"], self.game_ui.assets['mars_hex_select_01'])
        if self.save_data['l1'] == 1:
            l2_button = ui.Button(self.game_ui, 32, 32, (250, 200), 'l2', self.game_ui.assets["mars_hex_01"], self.game_ui.assets['mars_hex_select_01'])
        if self.save_data['l2'] == 1:
            l3_button = ui.Button(self.game_ui, 32, 32, (400, 150), 'l3', self.game_ui.assets["mars_hex_01"], self.game_ui.assets['mars_hex_select_01'])

        while True:
            if self.map_ended:
                break
            # Here is where we can draw our background
            self.screen.fill(self.bg_color)
            self.display.fill(self.bg_color)
            self.display.blit(pygame.transform.scale(self.game_ui.assets["planet_bg"], (self.display.get_size()[1], self.display.get_size()[1])), (150, 0))

            # here is where we manage the mouse position input
            self.screen_mpos = pygame.mouse.get_pos()[0] / self.render_scale, pygame.mouse.get_pos()[1] / self.render_scale

            # Here we display our UI
            for button in self.game_ui.buttons:
                button.draw_button(self.display)
                if button.check_hover():
                    button.draw_button_hover(self.display)

            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.game_ui.check_click() == 'l1':
                            self.selected_level = 1
                        elif self.game_ui.check_click() == 'l2':
                            self.selected_level = 2
                        elif self.game_ui.check_click() == 'l3':
                            self.selected_level = 3
                        if self.selected_level is not None:
                            self.game = main.Game()
                            self.game.current_level = self.levels[self.selected_level - 1][0]
                            self.game.run()
                            self.map_ended = True

            # Here we display our mouse
            self.display.blit(self.game_ui.assets['mouse_pointer'], self.screen_mpos)

            self.screen.blit(pygame.transform.scale(self.display, (1280, 720)), (0, 8))
            draw_text(self.screen, 'Level 1', self.text_font, (255, 255, 255), 560, 185)
            if self.save_data['l1'] == 1:
                draw_text(self.screen, 'Level 2', self.text_font, (255, 255, 255), 460, 385)
            if self.save_data['l2'] == 1:
                draw_text(self.screen, 'Level 3', self.text_font, (255, 255, 255), 765, 285)

            pygame.display.update()
            self.dt = self.clock.tick(FPS) / 1000
