import pygame
from scripts.utils import load_image


class UI:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.mpos = game.screen_mpos

    def create_buttons(self):
        # This is for my pc
        if self.game.screen.get_size()[0] == 2560 and self.game.screen.get_size()[1] == 1440:
            pause_button = Button(self, 32, 32, (2250, 50), 'pause', self.game.assets["pause_button"])
            start_button = Button(self, 32, 32, (2350, 50), 'play', self.game.assets["play_button"])
            fast_forward_button = Button(self, 32, 32, (2450, 50), 'fast_forward',
                                         self.game.assets["fast_forward_button"])
            tower_button = Button(self, 128, 128, (2225, 500), 'tower_button', self.game.assets["tower_button"])
            gem_button = Button(self, 128, 128, (2400, 500), 'gem_button', self.game.assets["gem_button"])
        # This is for my laptop
        if self.game.screen.get_size()[0] == 1440 and self.game.screen.get_size()[1] == 900:
            pause_button = Button(self, 32, 32, (1150, 50), 'pause', self.game.assets["pause_button"])
            start_button = Button(self, 32, 32, (1250, 50), 'play', self.game.assets["play_button"])
            fast_forward_button = Button(self, 32, 32, (1350, 50), 'fast_forward',
                                         self.game.assets["fast_forward_button"])
        if self.game.screen.get_size()[0] == 1280 and self.game.screen.get_size()[1] == 720:
            pause_button = Button(self, 32, 32, (1100, 20), 'pause', self.game.assets["pause_button"])
            start_button = Button(self, 32, 32, (1165, 20), 'play', self.game.assets["play_button"])
            fast_forward_button = Button(self, 32, 32, (1230, 20), 'fast_forward',
                                         self.game.assets["fast_forward_button"])
            tower_button = Button(self, 64, 64, (1100, 300), 'tower_button', self.game.assets["tower_button_small"])
            gem_button = Button(self, 64, 64, (1200, 300), 'gem_button', self.game.assets["gem_button_small"])

    def check_click(self):
        if len(self.buttons) > 0:
            for button in self.buttons:
                # Check if we have a collision with the mpos point
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    return button.name
        else:
            print("No buttons were found when checking for click")


class Button:
    def __init__(self, ui, width, height, pos, name, img):
        self.ui = ui
        self.width, self.height = width, height
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.img = img
        self.name = name
        ui.buttons.append(self)

    def button_presed(self, action):
        print("We clicked on a button")

    def draw_button(self):
        self.ui.game.screen.blit(self.img, self.pos)


def button_pressed(self, button):
    print(r"Button: {button} pressed")





