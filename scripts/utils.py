import os
import pygame

BASE_IMG_PATH = r"C:/Users/nicho/PycharmProjects/py_game_tower_defense/art/"


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


# This script loads a whole folder of images based on the specified folder
def load_images(path):
    images = []
    print(BASE_IMG_PATH + path)
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images


def draw_grid(self):
    # Here is where we are initializing the bg and bg grid
    '''
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
    '''
