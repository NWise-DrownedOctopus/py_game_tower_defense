import pygame
import sys
import json
from scripts.utils.assets import load_image
from scripts.utils.ui_utils import draw_text
from scripts.utils.save import load_save, create_save
from pygame.locals import K_ESCAPE, MOUSEBUTTONDOWN
from scripts import ui
import map

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
pygame.display.set_caption("game base")
screen = pygame.display.set_mode((1280, 720), 0, 32)
clock = pygame.time.Clock()
button_1_size = [500, 110]

font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 50)

click = False
assets = {
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

def main_menu():
    # play_audio('BGM_Menu', True)
    menu_ui = ui.UI("main_menu", pygame.display)
    if pygame.display.get_surface().get_width() == 1280 and pygame.display.get_surface().get_height() == 720:
        button_1_pos = [510, 450]
        button_2_pos = [510, 600]
        new_game_button = ui.Button(menu_ui, 500, 110, (button_1_pos[0], button_1_pos[1]), 'new_game')
        continue_button = ui.Button(menu_ui, 500, 110, (button_2_pos[0], button_2_pos[1]), 'continue')
    # menu_ui.create_menu_buttons(screen)
    while True:
        bg = assets['background'].copy()
        screen.blit(pygame.transform.scale(bg, (1310, 720)), (-20, 0))
        draw_text(screen, 'ERROUR', menu_ui.font, menu_ui.font_color, 480, 100)
        draw_text(screen, 'NEW GAME', menu_ui.sub_font, menu_ui.font_color, button_1_pos[0], button_1_pos[1])
        draw_text(screen, 'CONTINUE', menu_ui.sub_font, menu_ui.font_color, button_2_pos[0], button_2_pos[1])
        for button in menu_ui.buttons:
            button.draw_button(screen)

        mx, my = pygame.mouse.get_pos()
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
                    save_data = load_save('data/save.json')
                    map.Map(save_data).run()
                    break
                elif clicked == 'continue':
                    save_data = load_save('data/save.json')
                    map.Map(save_data).run()
                    break

        pygame.display.update()
        clock.tick(60)

main_menu()
