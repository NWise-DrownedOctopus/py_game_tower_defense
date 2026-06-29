import pygame
import sys
import asyncio
from scripts.utils.assets import load_image
from scripts.utils.ui_utils import draw_text
from scripts.utils.save import load_save, create_save
from pygame.locals import K_ESCAPE, MOUSEBUTTONDOWN
from scripts import ui

FPS = 60

class MainMenu:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.clock = app.clock
        self.assets = {
            'button': load_image("ui/button_02_06.png"),
            'button_hover': load_image("ui/button_02_05.png"),
            'button_clicked': load_image("ui/button_02_04.png"),
            'button_back': load_image("ui/button_02_02.png"),
            'buttonFrame': load_image("ui/button_02_03.png"),
            "background": load_image("ui/bg.png"),
            'title': load_image("ui/el_04_04.png"),
            'title_frame': load_image("ui/el_04_01.png"),
            'title_frame_2': load_image("ui/el_04_03.png"),
        }
            
    async def run(self):
        from scripts.utils.audio import play_audio
        play_audio('BGM_Menu', loop=True)
        menu_ui = ui.UI("main_menu", self.screen)
        button_1_pos = [510, 450]
        button_2_pos = [510, 600]
        new_game_button = ui.Button(menu_ui, 500, 110, (button_1_pos[0], button_1_pos[1]), 'new_game')
        continue_button = ui.Button(menu_ui, 500, 110, (button_2_pos[0], button_2_pos[1]), 'continue')
        while True:
            bg = self.assets['background'].copy()
            self.screen.blit(pygame.transform.scale(bg, (1310, 720)), (-20, 0))
            draw_text(self.screen, 'ERROUR', menu_ui.font, menu_ui.font_color, 480, 100)
            draw_text(self.screen, 'NEW GAME', menu_ui.sub_font, menu_ui.font_color, button_1_pos[0], button_1_pos[1])
            draw_text(self.screen, 'CONTINUE', menu_ui.sub_font, menu_ui.font_color, button_2_pos[0], button_2_pos[1])
            for button in menu_ui.buttons:
                button.draw_button(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    clicked = menu_ui.check_click()                
                    if clicked == 'new_game':
                        create_save('data/save.json')
                        self.app.save_data = load_save('data/save.json')
                        return 'map'
                    elif clicked == 'continue':
                        self.app.save_data = load_save('data/save.json')
                        return 'map'

            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)
