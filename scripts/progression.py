def complete_level(save_data, level_key, unlocks):
    save_data["levels"][level_key]["completed"] = True
    for next_level in unlocks:
        if next_level in save_data["levels"]:
            save_data["levels"][next_level]["unlocked"] = True
    return save_data