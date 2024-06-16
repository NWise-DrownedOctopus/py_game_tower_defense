import pygame
from scripts.utils import load_image


class UI:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.mpos = game.screen_mpos

    def create_buttons(self):
        pause_button = Button(self, 32, 32, (1150, 50), self.game.assets["pause_button"])
        start_button = Button(self, 32, 32, (1250, 50), self.game.assets["play_button"])
        fast_forward_button = Button(self, 32, 32, (1350, 50), self.game.assets["fast_forward_button"])

    def update(self):
        pass

    def check_click(self):
        if len(self.buttons) > 0:
            for button in self.buttons:
                # Check if we have a collision with the mpos point
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.button_presed(print())
        else:
            print("No buttons were found when checking for click")


class Button:
    def __init__(self, ui, width, height, pos, img):
        self.ui = ui
        self.width, self.height = width, height
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        ui.buttons.append(self)

    def button_presed(self, action):
        print("We clicked on a button")

    def draw_button(self):
        self.ui.game.screen.blit(self.img, self.pos)


def button_pressed(self, button):
    print(r"Button: {button} pressed")





