import json
import os


class FavoritesManager:

    def __init__(self):
        self.file_path = "favorites.json"

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def get_favorites(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def add_favorite(self, city):
        data = self.get_favorites()

        if city not in data:
            data.append(city)

        with open(self.file_path, "w") as f:
            json.dump(data, f)

    def remove_favorite(self, city):
        data = self.get_favorites()

        if city in data:
            data.remove(city)

        with open(self.file_path, "w") as f:
            json.dump(data, f)