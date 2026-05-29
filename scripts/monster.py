import pygame
from scripts.healthBar import HealthBar
from scripts.utils import play_audio
from pathfinding import Pathfinding


class Monster (pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, pathfinding, render_scale, m_type):
        super().__init__()
        self.m_type = m_type
        self.pos = (int(x_pos), int(y_pos))
        self.screen_pos = self.pos[0] * 32 * render_scale, self.pos[1] * 32 * render_scale
        self.current_rotation = 0

        if self.m_type == "big":
            self.max_health = 30
            self.monster_img = pygame.image.load('art/monsters/monsters_22.png')
            self.monster_move_speed = .02
            self.steel_value = 12
            self.base_hit_cost = 80
        elif self.m_type == "fast":
            self.max_health = 5
            self.monster_img = pygame.image.load('art/monsters/monsters_26.png')
            self.monster_move_speed = .1
            self.steel_value = 2
            self.base_hit_cost = 5
        else:
            self.max_health = 10
            self.monster_img = pygame.image.load('art/monsters/monsters_20.png')
            self.monster_move_speed = .05
            self.steel_value = 8
            self.base_hit_cost = 10

        self.current_health = self.max_health
        self.healthBar = HealthBar(self, self.screen_pos[0], self.screen_pos[1])
        self.monster_mask = pygame.mask.from_surface(self.monster_img)
        self.pathfinding = pathfinding
        self.game = pathfinding.game
        self.target_pos = None
        self.target_rotation = 0
        self.pathway = None
        self.pathway_index = 0
        self.is_dead = False

    def dmg(self, dmg):
        self.current_health -= dmg
        if self.current_health <= 0:
            del self

    def draw(self, surface):
        # print("Current current rotation = ", self.current_rotation)
        if self.current_rotation != self.target_rotation:
            delta_rotation = (self.current_rotation - self.target_rotation)
            self.monster_img = pygame.transform.rotate(self.monster_img, delta_rotation)
            self.current_rotation = self.target_rotation
        surface.blit(self.monster_img, self.screen_pos)
        if self.current_health < self.max_health:
            self.healthBar.draw(surface, self.screen_pos)

    def find_path(self):
        self.pathway = []
        for tile in self.pathfinding.pathway:
            self.pathway.append([str(tile.row), str(tile.col)])
        self.pathway.reverse()
        self.target_pos = (int(self.pathway[self.pathway_index][0]), int(self.pathway[self.pathway_index][1]))

    def update(self):
        # we don't need to update anything if the game is paused, so let's return if that's the case
        if self.game.paused:
            return

        # let us get destroyed if we have zero health remaining
        if self.current_health <= 0:
            self.kill()
            self.game.current_steel += self.steel_value
            self.is_dead = True
            play_audio('death_1')
            return

        # Here we want to move our monsters position towards our target position
        # Our target position is always going to be the next index of our pathway
        # we start the game at index 0, and then move towards index 1 ect.

        # let's check if we made it to our finally destination
        if self.pathway is None:
            return
        if self.pathway_index == len(self.pathway) - 1:
            self.kill()
            self.game.current_steel -= self.base_hit_cost
            play_audio('death_2')
            return

        # first lets check to see if we are within a reasonable distance to our target
        self.pos = (float(self.pos[0]), float(self.pos[1]))
        self.target_pos = (float(self.target_pos[0]), float(self.target_pos[1]))
        threshold = .1
        if abs(self.pos[0] - self.target_pos[0]) <= threshold and abs(self.pos[1] - self.target_pos[1]) <= threshold:
            self.pos = self.target_pos
            self.pathway_index += 1
            self.target_pos = self.pathway[self.pathway_index]

        self.pos = (float(self.pos[0]), float(self.pos[1]))
        self.target_pos = (float(self.target_pos[0]), float(self.target_pos[1]))
        # Now let us consider what we should do in the event that we are not at, or close to our target location
        # We want to move towards the location, and our target is going to be in one of four locations
        if self.game.fast_forward:
            # 1. Above us
            if self.target_pos[0] == self.pos[0] and self.target_pos[1] < self.pos[1]:
                # print("Target position is above us")
                self.target_rotation = 270
                self.pos = (self.pos[0], self.pos[1] - (self.monster_move_speed * 2))
            # 2. To our right
            elif self.target_pos[0] > self.pos[0] and self.target_pos[1] == self.pos[1]:
                # print("Target position is to our right")
                self.target_rotation = 0
                self.pos = (self.pos[0] + (self.monster_move_speed * 2), self.pos[1])
            # 3. Below us
            elif self.target_pos[0] == self.pos[0] and self.target_pos[1] > self.pos[1]:
                # print("Target position is below us")
                self.target_rotation = 90
                self.pos = (self.pos[0], self.pos[1] + (self.monster_move_speed * 2))
            # 4. To our Left
            elif self.target_pos[0] < self.pos[0] and self.target_pos[1] == self.pos[1]:
                # print("Target position is to our left")
                self.target_rotation = 180
                self.pos = (self.pos[0] - (self.monster_move_speed * 2), self.pos[1])
            # if none of these things our true, then we have gone off the grid
            else:
                raise ValueError(print("Target position is out of bounds, target position is off grid"))
        else:
            # 1. Above us
            if self.target_pos[0] == self.pos[0] and self.target_pos[1] < self.pos[1]:
                # print("Target position is above us")
                self.target_rotation = 270
                self.pos = (self.pos[0], self.pos[1] - self.monster_move_speed)
            # 2. To our right
            elif self.target_pos[0] > self.pos[0] and self.target_pos[1] == self.pos[1]:
                # print("Target position is to our right")
                self.target_rotation = 0
                self.pos = (self.pos[0] + self.monster_move_speed, self.pos[1])
            # 3. Below us
            elif self.target_pos[0] == self.pos[0] and self.target_pos[1] > self.pos[1]:
                # print("Target position is below us")
                self.target_rotation = 90
                self.pos = (self.pos[0], self.pos[1] + self.monster_move_speed)
            # 4. To our Left
            elif self.target_pos[0] < self.pos[0] and self.target_pos[1] == self.pos[1]:
                # print("Target position is to our left")
                self.target_rotation = 180
                self.pos = (self.pos[0] - self.monster_move_speed, self.pos[1])
            # if none of these things our true, then we have gone off the grid
            else:
                raise ValueError(print("Target position is out of bounds, target position is off grid"))

        self.screen_pos = self.pos[0] * 32, self.pos[1] * 32


