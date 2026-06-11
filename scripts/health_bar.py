import pygame

class HealthBar:
    width = 10
    height = 2
    dmg_color = pygame.Color(255, 0, 175)
    health_color = pygame.Color(0, 255, 0)

    def __init__(self, v_offset=1, h_offset=3):
        self.v_offset = v_offset
        self.h_offset = h_offset

    def draw(self, surface, pos, ratio):
        position = (pos[0] + self.h_offset, pos[1] - self.v_offset)
        health_width = self.width * ratio
        pygame.draw.rect(surface, self.dmg_color, (position[0], position[1], self.width, self.height))
        pygame.draw.rect(surface, self.health_color, (position[0], position[1], health_width, self.height))
