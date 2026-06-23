import pygame

def play_audio(sound, sfx_assets, loop=False):
    if loop:
        pygame.mixer.music.load(sfx_assets[sound])
        pygame.mixer.music.play(-1, 0.0)
        return
    sfx_assets[sound].play()