from sprite import Sprite

class Pokemon:
    def __init__(self, name, type, sprite: Sprite):
        self.name = name
        self.type = type
        self.sprite = sprite

    def __str__(self):
        return f"{self.name} ({self.type})"