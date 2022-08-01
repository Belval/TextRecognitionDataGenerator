import random as rnd

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter


def generate(
    imagePath
):
    _img = Image.open(imagePath)
    _mask = Image.new("RGB", (_img.width, _img.height), (0, 0, 0))


    return _img, _mask
