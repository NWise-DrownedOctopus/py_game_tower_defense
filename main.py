import sys

import pygame

from scripts import tower
from scripts import monster
from scripts import gem
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

# monster details
monster_pos = [220, 200]
monster_movement = [False, False]
monster_v_movement = [False, False]

FPS = 60


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("tower defense game")

        self.SCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][0]
        self.SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0][1]
        self.bg_color = (25, 25, 25)

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode((1020, 960))

        self.display = pygame.Surface((510, 480))

        self.clock = pygame.time.Clock()

        # here we will import all the assets we need in our game at runtime
        self.assets = {
            'player': load_image("player.png"),
            'grass': load_images("grass"),
            'dirt': load_images("dirt")
        }

        # here is where we initialize our tilemap
        self.tilemap = Tilemap(self, tile_size=16)

        # Here is where we are going to work with our camera initialization
        self.scroll = [0, 0]

    def run(self):
        # Here is where we can draw our background
        self.display.fill(self.bg_color)
        self.tilemap.render(self.display, offset=self.scroll)

        # Here is where we can initialize the scene
        towers = pygame.sprite.Group()
        gems = pygame.sprite.Group()
        monsters = pygame.sprite.Group()

        # Here is where we initialize all of our static elements in the scene
        # I put them in relevant lists, so that they can be updated in batches
        tower1 = tower.Tower([100, 100], self.display)
        towers.add(tower1)
        gem1 = gem.Gem([100, 100], self.display, tower1)
        gems.add(gem1)

        # Here is where we initialize our dynamic elements
        monster1 = monster.Monster(self, monster_pos[0], monster_pos[1])
        monsters.add(monster1)

        # Here we enter the game loop, it is called "every frame"
        while True:
            # Here we start the loop by drawing the background of the scene first
            self.display.fill(self.bg_color)

            # Here is where we control our camera movement based on player position
            self.scroll[0] += (monster1.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (monster1.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

            # here is where we render our tile map
            self.tilemap.render(self.display, offset=self.scroll)

            # Here is where we draw our static elements to the screen
            for player_tower in towers:
                player_tower.update(offset=self.scroll)
            for player_gem in gems:
                player_gem.update(offset=self.scroll)

            # Here is where we update the position of the monster
            monster1.update(self.display, monster_pos)
            monster_pos[0] += (monster_movement[1] - monster_movement[0]) * monster1.monster_move_speed
            monster_pos[1] += (monster_v_movement[1] - monster_v_movement[0]) * monster1.monster_move_speed

            # Here is where we check if the monster is in range of the turret
            for p_tower in towers:
                for e_monster in monsters:
                    p_tower.detect_monster(e_monster, offset=self.scroll)
            for p_gem in gems:
                p_gem.update(offset=self.scroll)

            # Here we update our projectiles
            for player_gem in gems:
                for projectile in player_gem.projectiles:
                    projectile.update(offset=self.scroll)

            # This is the event checker for each frame
            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        monster_movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        monster_movement[1] = True
                    if event.key == pygame.K_UP:
                        monster_v_movement[0] = True
                    if event.key == pygame.K_DOWN:
                        monster_v_movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        monster_movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        monster_movement[1] = False
                    if event.key == pygame.K_UP:
                        monster_v_movement[0] = False
                    if event.key == pygame.K_DOWN:
                        monster_v_movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(FPS)


Game().run()
