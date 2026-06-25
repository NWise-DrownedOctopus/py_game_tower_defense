import json

import json

def load_save(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Save file not found: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Save file is malformed: {e}")
        return None
    except PermissionError:
        print(f"Permission denied when loading save file: {path}")
        return None

def save_game(path, level, save_data):
    try:
        save_data[level] = 1
        with open(path, 'w') as f:
            json.dump(save_data, f)
    except PermissionError:
        print(f"Permission denied when saving game to {path}")
    except OSError as e:
        print(f"Failed to save game: {e}")

def load_monsters(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Monster data file not found: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Monster data file is malformed: {e}")
        return None
    except PermissionError:
        print(f"Permission denied when loading monster data: {path}")
        return None
    
def create_save(path):
    try:
        with open(path, 'w') as f:
            json.dump({'l1': 0, 'l2': 0, 'l3': 0}, f)
    except PermissionError:
        print(f"Permission denied when creating save file at {path}")
    except OSError as e:
        print(f"Failed to create save file: {e}")
    with open(path, 'w') as f:
        json.dump({'l1': 0, 'l2': 0, 'l3': 0}, f)