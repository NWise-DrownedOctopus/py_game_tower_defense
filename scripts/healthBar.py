import pygame


class HealthBar:
    width = 30
    height = 5
    dmg_color = pygame.Color(255, 0, 175)
    health_color = pygame.Color(0, 255, 0)

    def __init__(self, monster_target, obj_x=0, obj_y=0, offset=5):
        if obj_x == 0 or obj_y == 0:
            raise ValueError("Do we not have a target for the health bar?")
        self.position = (obj_x, obj_y - offset)
        self.monster_target = monster_target

    def draw_health_bar(self, surface):
        health_width = self.width * (self.monster_target.current_health / self.monster_target.max_health)
        pygame.draw.rect(surface, self.dmg_color, (self.position[0], self.position[1], self.width, self.height))
        pygame.draw.rect(surface, self.health_color, (self.position[0], self.position[1], health_width, self.height))
