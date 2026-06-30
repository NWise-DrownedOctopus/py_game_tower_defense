import json

DEFAULT_SAVE = {
    "version": 1,
    "levels": {
        "level_01": {"unlocked": True, "completed": False},
        "level_02": {"unlocked": False, "completed": False},
        "level_03": {"unlocked": False, "completed": False}
    },
    "persistent_resources": {
        "crystals": 0
    },
    "upgrade_tree": {},
    "bags": {
        "tier_1": {
            "fire": 2,
            "frost": 2,
            "poison": 1
        }
    }
}

def create_save(path):
    try:
        with open(path, 'w') as f:
            json.dump(DEFAULT_SAVE, f, indent=4)
    except PermissionError:
        print(f"Permission denied when creating save file at {path}")
    except OSError as e:
        print(f"Failed to create save file: {e}")

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

def save_game(path, save_data):
    try:
        with open(path, 'w') as f:
            json.dump(save_data, f, indent=4)
    except PermissionError:
        print(f"Permission denied when saving game to {path}")
    except OSError as e:
        print(f"Failed to save game: {e}")
        
def validate_save(save_data):
    for key, default in DEFAULT_SAVE.items():
        if key not in save_data:
            save_data[key] = default
    return save_data