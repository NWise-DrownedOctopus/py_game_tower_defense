import pygame
from scripts.utils import load_image, load_images


class Tower (pygame.sprite.Sprite):

    def __init__(self, pos, tile_pos, surface, game):
        super().__init__()
        pygame.init()
        self.attack_speed = 2
        self.pos = pos
        self.tile_pos = tile_pos
        self.surface = surface
        self.tower_img = load_image('Tower.png')
        self.has_gem = False

    def draw(self):
        self.surface.blit(self.tower_img, self.pos)
