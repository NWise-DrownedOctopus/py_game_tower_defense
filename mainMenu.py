import pygame, sys
from scripts.utils import load_image, draw_text
import map

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("game base")
screen = pygame.display.set_mode((1280, 720), 0, 32)
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 50)

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
    while True:
        bg = assets['background'].copy()
        screen.blit(pygame.transform.scale(bg, (1310, 720)), (-20, 0))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(505, 605, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                map.Map().run()
        if button_2.collidepoint((mx, my)):
            if click:
                pass
        # Start button
        button_frame_img = assets['buttonFrame'].copy()
        button_frame_img.set_colorkey((255,255,255))
        screen.blit(pygame.transform.scale(button_frame_img, (210, 70)), (500, 600))
        button_img = assets['button'].copy()
        button_img.set_colorkey((255, 255, 255))
        screen.blit(pygame.transform.scale(button_img, (200, 50)), (505, 605))
        draw_text(screen, 'Play', font, (255, 255, 255), 565, 615)

        # Title
        title_frame = assets['title'].copy()
        title_frame.set_colorkey((255, 255, 255))
        screen.blit(pygame.transform.scale(title_frame, (250, 80)), (480, 90))
        title_frame = assets['title_frame'].copy()
        title_frame.set_colorkey((255, 255, 255))
        screen.blit(pygame.transform.scale(title_frame, (250, 80)), (480, 90))

        draw_text(screen, 'Main Menu', font, (255, 255, 255), 515, 110)

        click = False

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
                    click = True

        pygame.display.update()
        clock.tick(60)


main_menu()
