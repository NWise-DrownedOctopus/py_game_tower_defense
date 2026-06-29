import json
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
        self.level_data = None
        self.wave_length = 14  # if I make this too short, we could run into an issue with not spawning enough
        self.last_wave_start = time.time()
        self.spawn_delay = None
        self.remaining_spawns = 0
        self.waves_finished = False
        self.map = None
        self.monster_spawn_pos = None
        self.base_pos = None

    def load(self, path):
        with open(path, 'r') as f:
            self.level_data = json.load(f)        
        
    def start(self):
        self.unlocks = self.level_data.get('unlocks', [])
        self.name = self.level_data['name']
        self.waves = self.level_data['waves']
        self.starting_towers = self.level_data['starting_towers']
        self.starting_gems = self.level_data['starting_gems']
        self.map = self.level_data['map']
        self.waves_finished = False
        self.game.level_ended = False
        self.game.paused = True
        self.monster_spawn_pos = self.level_data['monster_spawn_pos']
        self.base_pos = self.level_data['base_pos']
        self.current_wave = 0
        self.remaining_spawns = int(self.waves[self.current_wave][0])
        self.start_wave()

    def start_wave(self):
        self.spawn_delay = self.wave_length / int(self.waves[self.current_wave][0])
        self.remaining_spawns = int(self.waves[self.current_wave][0])

    def update(self):
        if self.game.paused:
            self.last_spawn += self.game.dt
            self.last_wave_start += self.game.dt
        if not self.game.paused and not self.waves_finished:
            if (time.time() - self.last_wave_start) > self.wave_length:
                if self.current_wave + 1 >= len(self.waves):
                    self.waves_finished = True
                    return
                self.current_wave += 1
                self.game.current_wave = self.current_wave
                self.start_wave()
                self.last_wave_start = time.time()                
            effective_delay = self.spawn_delay / 2 if self.game.fast_forward else self.spawn_delay
            if (time.time() - self.last_spawn) > effective_delay or self.remaining_spawns == int(
                    self.waves[self.current_wave][0]):
                if self.remaining_spawns == 0:
                    return
                self.game.spawn_monsters(self.waves[self.current_wave][1])
                self.last_spawn = time.time()
                self.remaining_spawns -= 1
        return