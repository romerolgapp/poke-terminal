from io import BytesIO

from PIL import Image
import aiohttp


class Sprite:
    def __init__(self, name: str, image_url: str):
        self._name = name
        self._image_url = image_url

    def __str__(self):
        return f"Sprite(name={self.name}, image_url={self.image_url})"
    
    @property
    def image_url(self) -> str:
        return self._image_url
    @property
    def name(self) -> str:
        return self._name

    @property
    def image(self) -> Image.Image:
        return self._image
    
    # Le pasamos el session para que no tenga que crear una nueva cada vez
    async def _fetch_image(self, aiohttp: aiohttp.ClientSession) -> Image.Image:
        async with aiohttp.get(self.image_url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch image from {self.image_url}: {response.status}")
            data = await response.read()
            self._image = Image.open(BytesIO(data))
            return self._image
        