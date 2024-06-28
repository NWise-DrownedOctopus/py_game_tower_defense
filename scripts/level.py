import json


class Level:
    def __init__(self, name):
        self.name = name
        self.waves = []
        self.starting_towers = []
        self.starting_gems = []
        self.current_wave = None

    def load(self, path):
        f = open(path, 'r')
        level_data = json.load(f)
        f.close()

        self.name = level_data['name']
        self.waves = level_data['waves']
        self.starting_towers = level_data['starting_towers']
        self.starting_gems = level_data['starting_gems']

        print(self.name)
        print(self.waves)
        print(self.starting_towers)
        print(self.starting_gems)

    def start_wave(self):
        pass


class Wave:
    def __init__(self):
        self.enemy_count = None

    def load_wave(self, filename):
        pass
