import cv2
import os
import random
import numpy as np

from PIL import Image, ImageFont, ImageDraw

def create_and_save_sample(index, text, font, out_dir, height):
    image_font = ImageFont.truetype(font=os.path.join('fonts', font), size=32)
    text_height, text_width = image_font.getsize(text)
    # We create our background a bit bigger than the text
    messy_background = create_messy_background(text_height + 10, text_width + 10)

    # We write the text on the image
    draw = ImageDraw.Draw(messy_background)

    draw.text((5, 5), text, fill=random.randint(0, 80), font=image_font)

    image_name = '{}_{}.jpg'.format(text, str(index))
    messy_background.save(os.path.join(out_dir, image_name))

def create_messy_background(height, width):
    """
        Create a background with Gaussian noise (to mimic paper)
    """

    # We create an all white image
    image = np.ones((width, height)) * 255

    # We had gaussian noise
    cv2.randn(image, 235, 10)
    
    return Image.fromarray(image).convert('L')