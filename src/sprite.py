from io import BytesIO

from PIL import Image
import numpy as np
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
    
    def crop_to_content(self) -> None:
        """Remove padding around the image. Uses alpha channel to find padding"""
        # using numpy as this is easier and also faster
        image_array = np.array(self.image)

        alpha_channel = image_array[:, :, 3]
        # first and last non transparent pixels taken as start and end
        # points for crop along both height and width axes
        non_zero_x_values, non_zero_y_values = alpha_channel.nonzero()
        top, left = np.min(non_zero_x_values), np.min(non_zero_y_values)
        bottom, right = np.max(non_zero_x_values), np.max(non_zero_y_values)
        cropped_image = image_array[top : bottom + 1, left : right + 1]

        self._image = Image.fromarray(cropped_image)
    def convert_to_rgba(self) -> None:
        if self.image.mode != "RGBA":
            rgba_image = self.image.convert("RGBA")
            self._image = rgba_image
    
    # Le pasamos el session para que no tenga que crear una nueva cada vez
    async def _fetch_image(self, aiohttp: aiohttp.ClientSession) -> Image.Image:
        async with aiohttp.get(self.image_url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch image from {self.image_url}: {response.status}")
            data = await response.read()
            self._image = Image.open(BytesIO(data))
            self.convert_to_rgba()
            self.crop_to_content()
            return self._image
        