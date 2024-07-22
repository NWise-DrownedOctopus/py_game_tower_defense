import pygame, sys, json
from scripts.utils import load_image, draw_text, play_audio
import map

mainClock = pygame.time.Clock()
from pygame.locals import *
from scripts import ui
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
    play_audio('BGM_Menu', True)
    menu_ui = ui.UI("main_menu")
    menu_ui.create_menu_buttons(screen)
    clicking = False
    while True:
        bg = assets['background'].copy()
        screen.blit(pygame.transform.scale(bg, (1310, 720)), (-20, 0))
        menu_ui.draw_menu_text(screen)
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
                if event.button == 1:
                    clicking = True
                if menu_ui.check_click() == 'new_game':
                    create_save('data/save.json')
                    save_data = load('data/save.json')
                    map.Map(save_data).run()
                    break
                if menu_ui.check_click() == 'continue':
                    save_data = load('data/save.json')
                    map.Map(save_data).run()
                    break

        pygame.display.update()
        clock.tick(60)


def load(path):
    f = open(path, 'r')
    save_data = json.load(f)
    f.close()
    return save_data


def create_save(path):
    f = open(path, 'w')
    json.dump({'l1': 0, 'l2': 0, 'l3': 0}, f)
    f.close()


main_menu()
