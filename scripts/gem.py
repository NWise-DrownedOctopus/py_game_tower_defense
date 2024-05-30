# Nicholas Wise
# https://stackoverflow.com/questions/50348125/creating-a-auto-targeting-bullet
import pygame
from pygame.math import Vector2
import time


class Gem (pygame.sprite.Sprite):
    gem_img = pygame.image.load('art/gem.png')

    def __init__(self, pos, surface, tower):
        super().__init__()
        self.pos = pos
        self.surface = surface
        self.tower = tower
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.gem_img_pos = [int(self.x_pos - (self.gem_img.get_width() / 2)),
                            int(self.y_pos - self.gem_img.get_height() / 2)]
        self.projectiles = pygame.sprite.Group()
        self.last_shot = time.time()
        self.shot_delay = 1

    def draw(self):
        self.surface.blit(self.gem_img, self.pos)

    def update(self):
        if self.tower.valid_target is not None:
            if time.time() - self.last_shot > self.shot_delay:
                self.fire(self.tower.valid_target)
                self.last_shot = time.time()
        # print(f"number of projectiles: {len(self.projectiles)}")

    def fire(self, monster):
        # print(f"Gem: {self} calling fire()")
        projectile = Projectile(self.gem_img_pos, monster, self.surface)
        self.projectiles.add(projectile)


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
        self.direction = (target.x_pos, target.y_pos) - self.position
        self.dmg = 2
        # print(f"Target Direction = {self.direction}")
        radius, angle = self.direction.as_polar()
        # print(f"Target radius = {radius}, angle = {angle}")
        self.img = pygame.transform.rotozoom(self.img, -angle-90, 1)
        # print(f"Projectile rotation: {-angle-90}")
        self.velocity = self.direction.normalize() * 11
        self.projectile_mask = pygame.mask.from_surface(self.img)

    def update(self):
        # print(f"Projectile: {self}, is starting at position {self.position}")
        self.direction = (self.target.x_pos, self.target.y_pos) - self.position
        self.velocity = self.direction.normalize() * 5
        new_position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.position = Vector2(new_position)
        self.rect.center = new_position  # And the rect.
        # print(f"Projectile: {self}, is ending at position {self.position}")
        self.screen_surface.blit(self.img, new_position)

        # Here we will handle what happens when we collide with a monster
        if self.projectile_mask.overlap(self.target.monster_mask, (self.target.x_pos - self.position[0], self.target.y_pos - self.position[1])):
            # print("Projectile has collided")
            self.target.dmg(self.dmg)
            self.kill()

        if not self.screen_rect.contains(self.rect):
            print(f"Killing projectile")
            self.kill()
