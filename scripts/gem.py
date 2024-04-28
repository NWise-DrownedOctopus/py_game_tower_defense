# Nicholas Wise
# https://stackoverflow.com/questions/50348125/creating-a-auto-targeting-bullet
import pygame
from pygame.math import Vector2


class Gem:
    gem_img = pygame.image.load('art/gem.png')

    def __init__(self, pos, surface, tower):
        self.pos = pos
        self.surface = surface
        self.tower = tower
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.gem_img_pos = [int(self.x_pos - (self.gem_img.get_width() / 2)),
                            int(self.y_pos - self.gem_img.get_height() / 2)]
        self.projectiles = []

    def draw(self):
        self.surface.blit(self.gem_img, self.gem_img_pos)

    def update(self):
        if self.tower.valid_target is not None:
            self.fire(self.tower.valid_target)
        print(f"number of projectiles: {len(self.projectiles)}")

    def fire(self, monster):
        print(f"Gem: {self} calling fire()")
        # projectile = Projectile(self.gem_img_pos, (monster.x_pos, monster.y_pos), self.surface)
        # self.projectiles.append(projectile)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target, screen_rect):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('art/bullet.png')
        self.target = target
        self.screen_surface = screen_rect
        self.screen_rect = screen_rect.get_rect()
        self.rect = self.img.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.direction = target - self.position
        print(f"Target Direction = {self.direction}")
        radius, angle = self.direction.as_polar()
        print(f"Target radius = {radius}, angle = {angle}")
        self.img = pygame.transform.rotozoom(self.img, -angle-90, 1)
        print(f"Projectile rotation: {-angle-90}")
        self.velocity = self.direction.normalize() * 11

    def update(self):
        print(f"Projectile: {self}, is starting at position {self.position}")
        self.direction = self.target - self.position
        self.velocity = self.direction.normalize() * 5
        new_position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.position = Vector2(new_position)
        self.rect.center = new_position  # And the rect.
        print(f"Projectile: {self}, is ending at position {self.position}")
        self.screen_surface.blit(self.img, new_position)

        if not self.screen_rect.contains(self.rect):
            print(f"Killing projectile")
            self.kill()
