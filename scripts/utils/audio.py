import sys
import pygame

BASE_AUDIO_PATH = "audio/"

def _get_audio_filename(filename):
    if sys.platform == "emscripten":
        name = filename.rsplit('.', 1)[0]
        return name + '.ogg'
    return filename

sfx_assets = None

def init_audio():
    global sfx_assets
    sfx_assets = {
        'fire': pygame.mixer.Sound(BASE_AUDIO_PATH + _get_audio_filename("laser_bolt.mp3")),
        'build': pygame.mixer.Sound(BASE_AUDIO_PATH + _get_audio_filename("build_noise.mp3")),
        'button': pygame.mixer.Sound(BASE_AUDIO_PATH + _get_audio_filename("button_press.mp3")),
        'death_1': pygame.mixer.Sound(BASE_AUDIO_PATH + _get_audio_filename("death_noise_1.mp3")),
        'death_2': pygame.mixer.Sound(BASE_AUDIO_PATH + _get_audio_filename("death_noise_2.mp3")),
        'BGM_Menu': BASE_AUDIO_PATH + _get_audio_filename("BGM_Menu.wav"),
        'BGM_Game_1': BASE_AUDIO_PATH + _get_audio_filename("BGM_Game_1.wav"),
        'BGM_Game_2': BASE_AUDIO_PATH + _get_audio_filename("BGM_Game_2.wav")
    }

def play_audio(sound, loop=False):
    if loop:
        pygame.mixer.music.load(sfx_assets[sound])
        pygame.mixer.music.play(-1, 0.0)
        return
    sfx_assets[sound].play()