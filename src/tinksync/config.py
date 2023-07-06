import json, os


def set_settings(new_settings):
    with open("settings.json", "w") as f:
        f.write(json.dumps(new_settings, indent=4))


def get_settings():
    with open("settings.json", "r") as f:
        return json.loads(f.read())
