#!/usr/bin/env python3

import asyncio
import subprocess
import aiohttp
from PIL import Image
from io import BytesIO
from pathlib import Path
from rich.console import Console
from tempfile import NamedTemporaryFile
from unicode_converter import UnicodeConverter
from type import render_type_badge

from sprite import Sprite

import numpy as np



console = Console()

#https://pokeapi.co/docs/v2#pokemon


async def generate_pokemon_sprite(pokemon_name):
    pokemon_type = []
    pokemon_type1 = "water"
    pokemon_type2 = "rock"
    pokemon_types = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
    url = f"https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/{pokemon_name}.png"
    #url = f"https://raw.githubusercontent.com/PMDCollab/SpriteCollab/master/portrait/0025/Dizzy.png"
    sprite = Sprite(pokemon_name, url)
    console.print(f"Generated sprite for {pokemon_name}: {sprite}")
    async with aiohttp.ClientSession() as session:
        image = await sprite._fetch_image(session)

    console.print(f"Fetched image for {pokemon_name}: {image}")
    image.show()
    converter = UnicodeConverter()
    unicode_sprite = converter.convert_image_to_unicode(image)
    console.print(f"Unicode sprite for {pokemon_name}:\n{unicode_sprite}")
    print (unicode_sprite)
    
    for pokemon_type in pokemon_types:
        badge = render_type_badge(pokemon_type)
        print(f"{pokemon_type} {badge}")
    print(f"{pokemon_name} {render_type_badge(pokemon_type1)} {render_type_badge(pokemon_type2)}")


if __name__ == "__main__":
    print("Hello, world!")
    asyncio.run(generate_pokemon_sprite("pikachu"))
