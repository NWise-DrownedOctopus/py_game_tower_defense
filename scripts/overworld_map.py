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
        pygame.mouse.set_visible(False)
        self.load('data/overworld_map.json')

        for level in self.levels:
            if self.app.save_data['levels'][level['key']]['unlocked']:
                ui.Button(self.game_ui, 32, 32, level['map_pos'], level['key'],
                        self.game_ui.assets["mars_hex_01"], 
                        self.game_ui.assets['mars_hex_select_01'])

        while True:
            self.screen.fill(self.bg_color)
            self.display.fill(self.bg_color)
            self.display.blit(pygame.transform.scale(
                self.game_ui.assets["planet_bg"], 
                (self.display.get_size()[1], self.display.get_size()[1])), (150, 0))

            self.screen_mpos = (pygame.mouse.get_pos()[0] / self.render_scale, 
                                pygame.mouse.get_pos()[1] / self.render_scale)

            for button in self.game_ui.buttons:
                button.draw_button(self.display)
                if button.check_hover():
                    button.draw_button_hover(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = self.game_ui.check_click()
                    if event.button == 1 and clicked:
                        for level in self.levels:
                            if clicked == level['key']:
                                self.app.current_level = level['file']
                                self.app.current_level_key = level['key']
                                return 'tower_defense'

            self.display.blit(self.game_ui.assets['mouse_pointer'], self.screen_mpos)

            self.screen.blit(pygame.transform.scale(self.display, (1280, 720)), (0, 8))
            for level in self.levels:
                if self.app.save_data['levels'][level['key']]['unlocked']:
                    draw_text(self.screen, level['label'], self.text_font, 
                            (255, 255, 255), level['label_pos'][0], level['label_pos'][1])

            pygame.display.update()
            self.dt = self.clock.tick(FPS) / 1000