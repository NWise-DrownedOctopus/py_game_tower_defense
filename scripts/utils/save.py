import json

def load_save(path):
    with open(path, 'r') as f:
        save_data = json.load(f)
        return save_data

def save_game(path, level, save_data):
    with open(path, 'r') as f:
        save_data[level] = 1
        json.dump(save_data, f)
    
def load_monsters(path):
    with open(path, 'r') as f:
        monster_data = json.load(f)
        return monster_data