import pygame
import time

from scripts.utils.assets import load_image, load_mask
from scripts.utils.audio import play_audio
from scripts.projectile import Projectile

class Gem (pygame.sprite.Sprite):

    def __init__(self, pos, tower, surf, game):
        super().__init__()
        self.pos = pos
        self.surf = surf
        self.tower = tower
        self.tower.gem = self
        self.projectiles = pygame.sprite.Group()
        self.last_shot = time.time()
        self.shot_delay = 1
        self.range = 100
        self.damage = 4
        self.projectile_speed = 4
        self.hit_count = 0
        self.game = game
        self.valid_target_gizmo = load_image('valid_target_gizmo.png')
        self.target_mask_gizmo = load_mask('target_mask_gizmo.png')
        self.valid_target_gizmo = pygame.transform.scale(self.valid_target_gizmo, (self.range * 2, self.range * 2))
        self.target_mask_gizmo = pygame.transform.scale(self.target_mask_gizmo, (self.range * 2, self.range * 2))
        self.gem_img = load_image('gem.png')
        self.range_mask = pygame.mask.from_surface(self.target_mask_gizmo)
        self.tile_size = self.game.tile_size
        self.targets = []
        self.game.hoverables.append(self)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.tile_size, self.tile_size)

    def draw(self):
        self.surf.blit(self.gem_img, self.pos)

    def update(self):
        if self.game.paused:
            self.last_shot += self.game.dt
        if len(self.targets) > 0 and not self.game.paused:
            current_target = self.targets[0]
            for target in self.targets:
                if target.pathway_index > current_target.pathway_index:
                    current_target = target
            delay = self.shot_delay / 2 if self.game.fast_forward else self.shot_delay
            if (time.time() - self.last_shot) > delay:
                if current_target in self.game.monsters:
                    self.fire(current_target)
                    self.hit_count += 1
                    self.last_shot = time.time()

    def on_hover(self):
        range_display_pos = (
            self.pos[0] + (self.tile_size / 2) - self.range, self.pos[1] + (self.tile_size / 2) - self.range)
        self.surf.blit(self.valid_target_gizmo, range_display_pos)

    def detect_monster(self):
        self.targets = []
        range_display_pos = (
            self.pos[0] + (self.tile_size / 2) - self.range, self.pos[1] + (self.tile_size / 2) - self.range)
        for monster in self.game.monsters:
            if self.range_mask.overlap(monster.monster_mask,
                                       (monster.screen_pos[0] - range_display_pos[0],
                                        monster.screen_pos[1] - range_display_pos[1])):
                if monster not in self.targets and not monster.is_dead:
                    self.targets.append(monster)

    def fire(self, monster):
        from scripts.utils.audio import sfx_assets
        projectile = Projectile(self.pos, monster, self.surf, self.damage, self.projectile_speed, self.game)
        self.projectiles.add(projectile)
        play_audio('fire')
