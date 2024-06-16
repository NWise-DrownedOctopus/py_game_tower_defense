import pygame
from scripts.utils import load_image


class UI:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.mpos = game.screen_mpos

    def update(self):
        pass

    def check_click(self):
        if len(self.buttons) > 0:
            for button in self.buttons:
                # Check if we have a collision with the mpos point
                if button.rect.collidepoint(self.mpos):
                    button.button_presed()
        else:
            print("No buttons were found when checking for click")


class Button:
    def __init__(self, ui, width, height, pos):
        self.ui = ui
        self.width, self.height = width, height
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.img = load_image('art/target_mask_gizmo.png')
        self.mask = pygame.mask.from_surface(self.img)
        ui.buttons.append(self)

    def start(self):

    def button_presed(self, action):
        action()


def button_pressed (self, button):
    print(r"Button: {button} pressed")





