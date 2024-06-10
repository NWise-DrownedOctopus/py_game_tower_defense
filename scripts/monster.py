import pygame
from scripts.healthBar import HealthBar
from pathfinding import Pathfinding


class Monster (pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, pathfinding, max_health=10):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.max_health = max_health
        self.current_health = 10
        self.healthBar = HealthBar(self, self.x_pos, self.y_pos)
        self.monster_img = pygame.image.load('art/centipede.png')
        self.monster_mask = pygame.mask.from_surface(self.monster_img)
        self.monster_move_speed = 2
        self.monster_movement = [False, False]
        self.pathfinding = pathfinding

    def dmg(self, dmg):
        # if self.healthBar is None:
        #     self.healthBar = HealthBar(self.x_pos, self.y_pos)
        self.current_health -= dmg
        if self.current_health <= 0:
            print("Monster should die now, it is at or below 0 health")

    def draw(self, surface, pos):
        surface.blit(self.monster_img, pos)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.healthBar.draw(surface, pos)

    def get_pos(self):
        return self.x_pos, self.y_pos

    def find_path(self):
        print(self.pathfinding.pathway)


    def update(self):
        pass
