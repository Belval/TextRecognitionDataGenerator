import cv2
import math
import os
import random
import numpy as np

from PIL import Image, ImageFont, ImageDraw, ImageFilter

def create_and_save_sample(index, text, font, out_dir, height, extension, skewing_angle, random_skew, blur, random_blur, background_type):
    image_font = ImageFont.truetype(font=os.path.join('fonts', font), size=32)
    text_width, text_height = image_font.getsize(text)

    txt_img = Image.new('L', (text_width, text_height), 255)

    txt_draw = ImageDraw.Draw(txt_img)

    txt_draw.text((0, 0), text, fill=random.randint(1, 80), font=image_font)

    random_angle = random.randint(0-skewing_angle, skewing_angle)

    rotated_img = txt_img.rotate(skewing_angle if not random_skew else random_angle, expand=1)

    new_text_width, new_text_height = rotated_img.size

    # We create our background a bit bigger than the text
    background = None

    if background_type == 0:
        background = create_gaussian_noise_background(new_text_height + 10, new_text_width + 10)
    elif background_type == 1:
        background = create_plain_white_background(new_text_height + 10, new_text_width + 10)
    else:
        background = create_quasicrystal_background(new_text_height + 10, new_text_width + 10)

    mask = rotated_img.point(lambda x: 0 if x == 255 or x == 0 else 255, '1')

    background.paste(rotated_img, (5, 5), mask=mask)

    # Create the name for our image
    image_name = '{}_{}.{}'.format(text, str(index), extension)

    # Resizing the image to desired format
    new_width = float(text_width + 10) * (float(height) / float(text_height + 10))
    image_on_background = background.resize((int(new_width), height), Image.ANTIALIAS)

    final_image = image_on_background.filter(
        ImageFilter.GaussianBlur(
            radius=(blur if not random_blur else random.randint(0, blur))
        )
    )

    # Save the image
    final_image.convert('RGB').save(os.path.join(out_dir, image_name))

def create_gaussian_noise_background(height, width):
    """
        Create a background with Gaussian noise (to mimic paper)
    """

    # We create an all white image
    image = np.ones((height, width)) * 255

    # We add gaussian noise
    cv2.randn(image, 235, 10)

    return Image.fromarray(image).convert('L')

def create_plain_white_background(height, width):
    """
        Create a plain white background
    """

    return Image.new("L", (width, height), 255)

def create_quasicrystal_background(height, width):
    """
        Create a background with quasicrystal (https://en.wikipedia.org/wiki/Quasicrystal)
    """

    image = Image.new("L", (width, height))
    pixels = image.load()

    frequency = random.random() * 30 + 20 # frequency
    phase = random.random() * 2 * math.pi # phase
    rotation_count = random.randint(10, 20) # of rotations

    for kw in range(width):
        y = float(kw) / (width - 1) * 4 * math.pi - 2 * math.pi
        for kh in range(height):
            x = float(kh) / (height - 1) * 4 * math.pi - 2 * math.pi
            z = 0.0
            for i in range(rotation_count):
                r = math.hypot(x, y)
                a = math.atan2(y, x) + i * math.pi * 2.0 / rotation_count
                z += math.cos(r * math.sin(a) * frequency + phase)
            c = int(255 - round(255 * z / rotation_count))
            pixels[kw, kh] = c # grayscale
    return image
