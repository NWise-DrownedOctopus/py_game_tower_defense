import pygame
import sys
import json
from scripts.utils.ui_utils import draw_text
from scripts import ui

FPS = 60

class OverworldMap:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.levels = None
        self.bg_color = (25, 25, 25)
        self.clock = app.clock
        self.render_scale = 2.0
        self.save_data = app.save_data
        self.screen_mpos = None
        self.text_font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 20)
        self.display = pygame.Surface((640, 360))
        self.dt = 0
        self.selected_level = None
        self.game_ui = ui.UI("ow_map", self.display)

    def load(self, path):
        try:
            with open(path, 'r') as f:
                map_data = json.load(f)
            self.levels = map_data['levels']
        except FileNotFoundError:
            print(f"Overworld map file not found: {path}")
            self.levels = []
        except json.JSONDecodeError as e:
            print(f"Overworld map file is malformed: {e}")
            self.levels = []
        except PermissionError:
            print(f"Permission denied when loading overworld map: {path}")
            self.levels = []

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
                    clicked = self.game_ui.check_click()
                    if event.button == 1:
                        if clicked == 'l1':
                            self.selected_level = 1
                        elif clicked == 'l2':
                            self.selected_level = 2
                        elif clicked == 'l3':
                            self.selected_level = 3
                        if self.selected_level is not None:
                            self.app.current_level = self.levels[self.selected_level - 1][0]
                            return 'tower_defense'

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
