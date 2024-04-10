import pygame


class Tower:
    tower_img = pygame.image.load('art/Tower.png')
    valid_target_gizmo = pygame.image.load('art/valid_target_gizmo.png')
    no_target_gizmo = pygame.image.load('art/no_target_gizmo.png')
    target_mask_gizmo = pygame.image.load('art/target_mask_gizmo.png')
    tower_mask = pygame.mask.from_surface(tower_img)
    range_mask = pygame.mask.from_surface(target_mask_gizmo)

    def __init__(self):
        pygame.init()
        self.damage = 10
        self.attack_speed = 2
        self.pos = [0, 0]

    def set_tower_position(self, pos):
        self.pos = pos
