import sys

import pygame


class Tower:
    tower_img = pygame.image.load('art/Tower.png')
    valid_target_gizmo = pygame.image.load('art/valid_target_gizmo.png')
    no_target_gizmo = pygame.image.load('art/no_target_gizmo.png')
    tower_mask = pygame.mask.from_surface(tower_img)
    range_mask = pygame.mask.from_surface(no_target_gizmo)
    attack_range = 300
    damage = 10
    attack_speed = 2
    pos = [0, 0]

    def __init__(self):
        pygame.init()

    def set_tower_position(self, pos):
        self.pos = pos


