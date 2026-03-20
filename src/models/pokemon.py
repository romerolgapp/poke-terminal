from sprite import Sprite

class Pokemon:
    def __init__(self, name, type: list, sprite: Sprite, height=None, weight=None, abilities=None, description=None):
        self.name = name
        self.type = type
        self.sprite = sprite
        self.height = height
        self.weight = weight
        self.abilities = abilities
        self.description = description

    def __str__(self):
        return f"{self.name} ({self.type})"