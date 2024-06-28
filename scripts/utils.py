import os
import pygame

BASE_IMG_PATH = r"art/"


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


# This script loads a whole folder of images based on the specified folder
def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images


def draw_text(surf, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surf.blit(img, (x, y))
