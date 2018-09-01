import cv2
import math
import random
import os
import numpy as np

from PIL import Image, ImageFont, ImageDraw, ImageFilter

class ComputerTextGenerator(object):
    @classmethod
    def generate(cls, text, font, text_color, font_size):
        image_font = ImageFont.truetype(font=font, size=font_size)
        text_width, text_height = image_font.getsize(text)

        txt_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))

        txt_draw = ImageDraw.Draw(txt_img)

        fill = random.randint(text_color[0], text_color[-1])

        txt_draw.text((0, 0), text, fill=(fill, fill, fill), font=image_font)

        return txt_img
