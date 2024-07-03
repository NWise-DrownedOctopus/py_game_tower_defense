# Nicholas Wise
# https://stackoverflow.com/questions/50348125/creating-a-auto-targeting-bullet
import pygame
from pygame.math import Vector2
import time


class Gem (pygame.sprite.Sprite):
    gem_img = pygame.image.load('art/gem.png')

    def __init__(self, pos, tower, surf, game):
        super().__init__()
        self.pos = pos
        self.surf = surf
        self.tower = tower
        self.projectiles = pygame.sprite.Group()
        self.last_shot = time.time()
        self.shot_delay = 1
        self.range = 80
        self.damage = 4
        self.game = game
        self.valid_target_gizmo = pygame.image.load('art/valid_target_gizmo.png')
        self.target_mask_gizmo = pygame.image.load('art/target_mask_gizmo.png')
        self.range_mask = pygame.mask.from_surface(self.target_mask_gizmo)
        self.tile_size = 16
        self.target_radius_pos = [int(self.pos[0]) - (self.target_mask_gizmo.get_width() / 2) + (self.tile_size / 2),
                                  int(self.pos[1]) - (self.target_mask_gizmo.get_height() / 2) + (self.tile_size / 2)]
        self.targets = []
        self.game.hoverables.append(self)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.tile_size, self.tile_size)

    def draw(self, range_display=False):
        self.surf.blit(self.gem_img, self.pos)

    def update(self):
        if self.game.paused:
            self.last_shot += self.game.dt
        if self.targets is not None and len(self.targets) > 0 and not self.game.paused:
            print(len(self.targets))
            current_target = self.targets[0]
            for target in self.targets:
                if target.pathway_index > current_target.pathway_index:
                    current_target = target
            if self.game.fast_forward:
                if (time.time() - self.last_shot) > (self.shot_delay / 2):
                    if current_target in self.game.monsters:
                        self.fire(current_target)
                        self.last_shot = time.time()
                        return
            if (time.time() - self.last_shot) > self.shot_delay:
                if current_target in self.game.monsters:
                    self.fire(current_target)
                    self.last_shot = time.time()

    def on_hover(self):
        range_display_pos = (
            self.pos[0] + (self.tile_size / 2) - self.range, self.pos[1] + (self.tile_size / 2) - self.range)
        self.valid_target_gizmo = pygame.transform.scale(self.valid_target_gizmo, (self.range * 2, self.range * 2))
        self.surf.blit(self.valid_target_gizmo, range_display_pos)

    def detect_monster(self):
        # print("According to our gem, there are ", len(self.targets), " monsters in range")
        self.targets = []
        range_display_pos = (
            self.pos[0] + (self.tile_size / 2) - self.range, self.pos[1] + (self.tile_size / 2) - self.range)
        self.target_mask_gizmo = pygame.transform.scale(self.target_mask_gizmo, (self.range * 2, self.range * 2))
        self.range_mask = pygame.mask.from_surface(self.target_mask_gizmo)
        for monster in self.game.monsters:
            # Here is where we check if the monster is in range of the turret
            if self.range_mask.overlap(monster.monster_mask,
                                       (monster.screen_pos[0] - range_display_pos[0],
                                        monster.screen_pos[1] - range_display_pos[1])):
                if monster not in self.targets and monster.is_dead == False:
                    self.targets.append(monster)
            else:
                if monster in self.targets:
                    self.targets.remove(monster)
            if monster.is_dead:
                self.targets.remove(monster)

    def fire(self, monster):
        projectile = Projectile(self.pos, monster, self.surf, self.damage)
        self.projectiles.add(projectile)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target, screen_rect, damage):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('art/bullet.png')
        self.target = target
        self.screen_surface = screen_rect
        self.screen_rect = screen_rect.get_rect()
        self.rect = self.img.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.direction = (target.screen_pos[0], target.screen_pos[1]) - self.position
        self.dmg = damage
        radius, angle = self.direction.as_polar()
        self.img = pygame.transform.rotozoom(self.img, -angle-90, 1)
        self.velocity = self.direction.normalize() * 11
        self.projectile_mask = pygame.mask.from_surface(self.img)

    def update(self):
        self.direction = (self.target.screen_pos[0], self.target.screen_pos[1]) - self.position
        self.velocity = self.direction.normalize() * 5
        new_position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.position = Vector2(new_position)
        self.rect.center = new_position  # And the rect.
        self.screen_surface.blit(self.img, new_position)

        # Here we will handle what happens when we collide with a monster
        if self.projectile_mask.overlap(self.target.monster_mask, (self.target.screen_pos[0] - self.position[0], self.target.screen_pos[1] - self.position[1])):
            # print("Projectile has collided")
            self.target.dmg(self.dmg)
            self.kill()

        if not self.screen_rect.contains(self.rect):
            print(f"Killing projectile")
            self.kill()
