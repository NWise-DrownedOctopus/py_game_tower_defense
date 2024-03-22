import sys

import pygame
from pygame.locals import *

# load art for test turret
tower_img = pygame.image.load('art/Tower.png')
tower_pos = [226, 222]

valid_target_gizmo = pygame.image.load('art/valid_target_gizmo.png')
# valid_target_gizmo.set_alpha(50)
no_target_gizmo = pygame.image.load('art/no_target_gizmo.png')
no_target_gizmo.set_alpha(50)
no_target_gizmo_mask = pygame.mask.from_surface(no_target_gizmo)


# monster details
monster_img = pygame.image.load('art/centipede.png')
monster_pos = [626, 222]
monster_end_pos = [300, 222]
monster_move_speed = 10
monster_movement = [False, False]
monster_mask = pygame.mask.from_surface(monster_img)

monster_pos = [int(monster_pos[0] - (monster_img.get_width() / 2)),
                            int(monster_pos[1] - monster_img.get_height() / 2)]
monster_end_pos = [int(monster_end_pos[0] - (monster_img.get_width() / 2)),
                                int(monster_end_pos[1] - monster_img.get_height() / 2)]

monster_sprite = pygame.sprite.Sprite()
monster_sprite.image = monster_img
monster_sprite.radius = (monster_img.get_width() / 2)

tower_image_pos = [int(tower_pos[0] - (tower_img.get_width() / 2)),
                   int(tower_pos[1] - tower_img.get_height() / 2)]
target_radius_pos = [int(tower_pos[0] - (no_target_gizmo.get_width() / 2)),
                     int(tower_pos[1] - no_target_gizmo.get_height() / 2)]

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("tower defense game")

        self.SCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][0]
        self.SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0][1]

        self.bg_border = 25
        self.bg_color = (25, 25, 25)
        self.game_bg_rect_width = self.SCREEN_WIDTH - (self.bg_border * 2)
        self.game_bg_rect_height = self.SCREEN_HEIGHT - (self.bg_border * 2)
        self.game_bg_rect = (self.bg_border, self.bg_border, self.game_bg_rect_width, self.game_bg_rect_height)

        self.bg_grid_width_count = 28
        self.bg_grid_height_count = 45
        self.bg_grid_color = (50, 50, 50)

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()


    def draw_grid(self):
        # Here is where we are initializing the bg and bg grid
        pygame.draw.rect(self.screen, self.bg_color, self.game_bg_rect)
        for count in range(self.bg_grid_width_count - 1):
            pygame.draw.line(self.screen, self.bg_grid_color,
                             (self.bg_border,
                              ((count + 1) * self.game_bg_rect_height / self.bg_grid_width_count + self.bg_border)),
                             ((self.game_bg_rect_width + self.bg_border),
                              ((count + 1) * self.game_bg_rect_height / self.bg_grid_width_count + self.bg_border)))

        for count in range(self.bg_grid_height_count - 1):
            pygame.draw.line(self.screen, self.bg_grid_color,
                             (((count + 1) * self.game_bg_rect_width / self.bg_grid_height_count + self.bg_border),
                              self.bg_border),
                             (((count + 1) * self.game_bg_rect_width / self.bg_grid_height_count + self.bg_border),
                              self.SCREEN_HEIGHT - self.bg_border))

    def run(self):
        while True:
            self.draw_grid()

            # Here is where we update the position of the monster
            self.screen.blit(monster_img, monster_pos)
            self.screen.blit(tower_img, tower_image_pos)
            monster_pos[0] += (monster_movement[1] - monster_movement[0]) * monster_move_speed

            # Here is where we check if the monster is in range of the turret
            if no_target_gizmo_mask.overlap(monster_mask, (monster_pos[0] - target_radius_pos[0], monster_pos[1] - target_radius_pos[1])):
                self.screen.blit(valid_target_gizmo, target_radius_pos)
            else:
                self.screen.blit(no_target_gizmo, target_radius_pos)

            # This is the event checker for each frame
            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        show_masks = not show_masks
                    if event.key == pygame.K_LEFT:
                        monster_movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        monster_movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        monster_movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        monster_movement[1] = False

            pygame.display.update()
            self.clock.tick(60)


Game().run()
