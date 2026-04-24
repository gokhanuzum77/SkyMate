import json
import os


class SettingsManager:
    def __init__(self):
        self.file_path = "settings.json"

        if not os.path.exists(self.file_path):
            self.reset_settings()

    def get_settings(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def save_settings(self, settings):
        with open(self.file_path, "w") as f:
            json.dump(settings, f)

    def set_theme(self, theme):
        settings = self.get_settings()
        settings["theme"] = theme
        self.save_settings(settings)

    def set_unit(self, unit):
        settings = self.get_settings()
        settings["unit"] = unit
        self.save_settings(settings)

    def set_default_city(self, city):
        settings = self.get_settings()
        settings["default_city"] = city
        self.save_settings(settings)

    def reset_settings(self):
        default_settings = {
            "theme": "Light",
            "unit": "metric",
            "default_city": "Yalova"
        }

        self.save_settings(default_settings)