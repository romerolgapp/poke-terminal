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

from sprite import Sprite

import numpy as np



console = Console()

#https://pokeapi.co/docs/v2#pokemon


async def generate_pokemon_sprite(pokemon_name):
    
    #url = f"https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/{pokemon_name}.png"
    url = f"https://raw.githubusercontent.com/PMDCollab/SpriteCollab/master/portrait/0222/Worried.png"
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



if __name__ == "__main__":
    print("Hello, world!")
    asyncio.run(generate_pokemon_sprite("pikachu"))
