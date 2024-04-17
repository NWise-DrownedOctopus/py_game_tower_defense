import pygame


class Tower:
    tower_img = pygame.image.load('art/Tower.png')
    valid_target_gizmo = pygame.image.load('art/valid_target_gizmo.png')
    no_target_gizmo = pygame.image.load('art/no_target_gizmo.png')
    target_mask_gizmo = pygame.image.load('art/target_mask_gizmo.png')
    tower_mask = pygame.mask.from_surface(tower_img)
    range_mask = pygame.mask.from_surface(target_mask_gizmo)
    debug_mode = False

    def __init__(self, pos, surface):
        pygame.init()
        self.damage = 10
        self.attack_speed = 2
        self.pos = [0, 0]
        self.surface = surface
        x_pos = pos[0]
        y_pos = pos[1]
        self.tower_image_pos = [int(x_pos - (self.tower_img.get_width() / 2)),
                                int(y_pos - self.tower_img.get_height() / 2)]
        self.target_radius_pos = [int(x_pos - (self.no_target_gizmo.get_width() / 2)),
                                  int(y_pos - self.no_target_gizmo.get_height() / 2)]
        surface.blit(self.tower_img, self.tower_image_pos)
        self.targets = []

    def detect_monster(self, monster):
        # Here is where we check if the monster is in range of the turret
        if self.range_mask.overlap(monster.monster_mask,
           (monster.x_pos - self.target_radius_pos[0], monster.y_pos - self.target_radius_pos[1])):
            self.surface.blit(self.valid_target_gizmo, self.target_radius_pos)
            print(F"Monster in range of {self.tower_img}")
        else:
            self.surface.blit(self.no_target_gizmo, self.target_radius_pos)
