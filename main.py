import pygame
import sys
from scripts.menu import MainMenu
from scripts.overworld_map import OverworldMap
from scripts.tower_defense import TowerDefense

class App:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.display.set_caption("Errour: Canto")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.save_data = None
        self.current_level = None
        self.current_level_key = None

    def run(self):
        scene = 'menu'
        while True:
            if scene == 'menu':
                scene = MainMenu(self).run()
            elif scene == 'map':
                scene = OverworldMap(self).run()
            elif scene == 'tower_defense':
                td = TowerDefense(self)
                td.current_level = self.current_level
                scene = td.run()
            elif scene == 'quit':
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    App().run()