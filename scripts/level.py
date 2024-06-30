import json
import pygame
import sys
import time

class Level:
    def __init__(self, game):
        self.name = None
        self.waves = []
        self.starting_towers = []
        self.starting_gems = []
        self.current_wave = None
        self.last_spawn = time.time()
        self.game = game
        self.wave_length = 12  # if I make this too short, we could run into an issue with not spawning enough
        self.last_wave_start = time.time()
        self.spawn_delay = 1
        self.remaining_spawns = 0
        self.waves_finished = False
        self.map = None

    def load(self, path):
        f = open(path, 'r')
        level_data = json.load(f)
        f.close()

        self.name = level_data['name']
        self.waves = level_data['waves']
        self.starting_towers = level_data['starting_towers']
        self.starting_gems = level_data['starting_gems']
        self.map = level_data['map']

        self.current_wave = '1'
        self.remaining_spawns = int(self.waves[self.current_wave])
        for key in self.waves:
            print("key: %s , type: %s" % (key, type(key)))

        print("Level Name: ", self.name)
        print("Waves: ", self.waves)
        print("number of waves: ", len(self.waves))
        print("map name: ", self.map)
        print("Starting towers: ", self.starting_towers)
        print("Starting gems", self.starting_gems)
        print("First Wave has ", self.remaining_spawns, " spawns")

    def start_wave(self):
        # self.spawn_delay = self.wave_length / (self.waves[self.current_wave] - 1)
        print(self.spawn_delay)
        self.remaining_spawns = int(self.waves[self.current_wave])

    def update(self):
        if self.game.paused:
            self.last_spawn += self.game.dt
            self.last_wave_start += self.game.dt
        if not self.game.paused and not self.waves_finished:
            # print("Wave last Start was ", time.time() - self.last_wave_start, " seconds ago")
            if (time.time() - self.last_wave_start) > self.wave_length:
                if self.current_wave >= str(len(self.waves)):
                    self.waves_finished = True
                    print("Waves finished spawning")
                    return
                print("We should move to next wave")
                self.current_wave = str(int(self.current_wave) + 1)
                self.game.current_wave = self.current_wave
                self.remaining_spawns = int(self.waves[self.current_wave])
                self.last_wave_start = time.time()
                # return
            # print("The time is: ", time.time())
            # print("last_spawn time is: ", self.last_spawn)
            # print('time - last_spawn = ', time.time() - self.last_spawn)
            # print('spawn_delay = ', self.spawn_delay)
            if (time.time() - self.last_spawn) > self.spawn_delay or self.remaining_spawns == int(self.waves[self.current_wave]):
                if self.remaining_spawns == 0:
                    return
                self.game.spawn_monsters()
                # print("Level just spawned a monster")
                self.last_spawn = time.time()
                self.remaining_spawns -= 1
        return


class Wave:
    def __init__(self):
        self.enemy_count = None

    def load_wave(self, filename):
        pass
