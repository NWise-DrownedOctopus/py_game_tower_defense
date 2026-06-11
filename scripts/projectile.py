import pygame
from pygame.math import Vector2
from scripts.utils import play_audio, get_image, get_sheet_dim, load_image

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target, screen_rect, damage, gem):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.frame = [0, 3]
        self.frame_width = 8
        self.frame_height = 8
        self.max_frame_width, self.max_frame_height = get_sheet_dim('projectile_img_sheet')
        self.img = get_image('projectile_img_sheet', self.frame, self.frame_width, self.frame_height)
        self.target = target
        self.gem = gem
        self.screen_surface = screen_rect
        self.screen_rect = screen_rect.get_rect()
        self.rect = self.img.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.direction = (target.screen_pos[0], target.screen_pos[1]) - self.position
        self.dmg = damage
        self.velocity = None
        self.projectile_mask = pygame.mask.from_surface(self.img)

    def update(self):
        if self.gem.game.paused:
            self.screen_surface.blit(self.img, self.position)
            return
        self.direction = (self.target.screen_pos[0] + 16, self.target.screen_pos[1] + 16) - self.position
        self.velocity = self.direction.normalize() * 4
        if self.gem.game.fast_forward:
            self.velocity = self.direction.normalize() * 8
        new_position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.position = Vector2(new_position)
        self.rect.center = new_position  # And the rect.
        self.frame[0] += 1
        if self.frame[0] >= self.max_frame_width:
            self.frame[0] = 0
        if self.frame[1] >= self.max_frame_height:
            self.frame[1] = 0
        self.img = get_image('projectile_img_sheet', self.frame, 8, 8)
        self.screen_surface.blit(self.img, new_position)

        # Here we will handle what happens when we collide with a monster
        if self.projectile_mask.overlap(self.target.monster_mask, (self.target.screen_pos[0] - self.position[0], self.target.screen_pos[1] - self.position[1])):
            self.target.dmg(self.dmg)
            self.kill()

        if not self.screen_rect.contains(self.rect):
            self.kill()
            