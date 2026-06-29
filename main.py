import pygame
import sys
import asyncio
from scripts.menu import MainMenu
from scripts.overworld_map import OverworldMap
from scripts.tower_defense import TowerDefense

class App:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(44100, -16, 2, 2048)
        from scripts.utils.audio import init_audio
        init_audio()
        pygame.display.set_caption("Errour: Canto")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.save_data = None
        self.current_level = None
        self.current_level_key = None

    async def run(self):
        scene = 'menu'
        while True:
            if scene == 'menu':
                scene = await MainMenu(self).run()
            elif scene == 'map':
                scene = await OverworldMap(self).run()
            elif scene == 'tower_defense':
                td = TowerDefense(self)
                td.current_level = self.current_level
                scene = await td.run()
            elif scene == 'quit':
                pygame.quit()
                sys.exit()
            await asyncio.sleep(0)

asyncio.run(App().run())