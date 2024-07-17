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
        self.monster_spawn_pos = None
        self.base_pos = None

    def load(self, path):
        f = open(path, 'r')
        level_data = json.load(f)
        f.close()

        self.name = level_data['name']
        self.waves = level_data['waves']
        self.starting_towers = level_data['starting_towers']
        self.starting_gems = level_data['starting_gems']
        self.map = level_data['map']
        self.waves_finished = False
        self.game.level_ended = False
        self.game.paused = True
        self.monster_spawn_pos = level_data['monster_spawn_pos']
        self.base_pos = level_data['base_pos']

        self.current_wave = '1'
        self.remaining_spawns = int(self.waves[self.current_wave][0])

        print("Level Name: ", self.name)
        print("Waves: ", self.waves)
        print("number of waves: ", len(self.waves))
        print("map name: ", self.map)
        print("Starting towers: ", self.starting_towers)
        print("Starting gems", self.starting_gems)
        print("First Wave has ", self.remaining_spawns, " spawns")

    def start_wave(self):
        print(self.spawn_delay)
        self.remaining_spawns = int(self.waves[self.current_wave][0])

    def update(self):
        if self.game.paused:
            self.last_spawn += self.game.dt
            self.last_wave_start += self.game.dt
        if not self.game.paused and not self.waves_finished:
            if (time.time() - self.last_wave_start) > self.wave_length:
                if self.current_wave >= str(len(self.waves)):
                    self.waves_finished = True
                    print("Waves finished spawning")
                    return
                print("We should move to next wave")
                self.current_wave = str(int(self.current_wave) + 1)
                self.game.current_wave = self.current_wave
                self.remaining_spawns = int(self.waves[self.current_wave][0])
                self.last_wave_start = time.time()
            if self.game.fast_forward:
                if (time.time() - self.last_spawn) > (self.spawn_delay / 2) or self.remaining_spawns == int(
                        self.waves[self.current_wave][0]):
                    if self.remaining_spawns == 0:
                        return
                    self.game.spawn_monsters(self.waves[self.current_wave][1])
                    self.last_spawn = time.time()
                    self.remaining_spawns -= 1
            else:
                if (time.time() - self.last_spawn) > self.spawn_delay or self.remaining_spawns == int(self.waves[self.current_wave][0]):
                    if self.remaining_spawns == 0:
                        return
                    self.game.spawn_monsters(self.waves[self.current_wave][1])
                    self.last_spawn = time.time()
                    self.remaining_spawns -= 1
        return


class Wave:
    def __init__(self):
        self.enemy_count = None

    def load_wave(self, filename):
        pass
