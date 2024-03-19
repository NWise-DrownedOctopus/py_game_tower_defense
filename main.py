import sys

import pygame

from scripts.tower import tower


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

        # load art for test turret
        self.tower = pygame.image.load('art/Tower.png')
        self.tower_pos = [120, 260]
        self.valid_target_gizmo = pygame.image.load('art/valid_target_gizmo.png')
        self.no_target_gizmo = pygame.image.load('art/no_target_gizmo.png')

        self.tower_image_pos = [int(self.tower_pos[0]-(self.tower.get_width()/2)), int(self.tower_pos[1]-self.tower.get_height()/2)]
        self.no_target_image_pos = [int(self.tower_pos[0]-(self.no_target_gizmo.get_width()/2)), int(self.tower_pos[1]-self.no_target_gizmo.get_height()/2)]

        print(self.tower_pos)
        print(self.tower_image_pos)
        print(self.no_target_image_pos)


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

            #self.screen.blit(self.tower, self.tower_image_pos)
            #self.screen.blit(self.no_target_gizmo, self.no_target_image_pos)
            # This is the event checker for each frame
            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)


Game().run()