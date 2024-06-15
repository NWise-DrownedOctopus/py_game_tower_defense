import pygame
from scripts.utils import load_image


class UI:
    def __init__(self, game):
        self.game = game
        self.buttons = []

    def update(self):
        pass


class Button:
    def __init__(self, ui, width, height, pos):
        self.ui = ui
        self.width, self.height = width, height
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.img = load_image('art/target_mask_gizmo.png')
        self.mask = pygame.mask.from_surface(self.img)
        ui.buttons.append(self)

    def button_presed(self, action):
        action()


def button_pressed (self, button):
    print(r"Button: {button} pressed")





