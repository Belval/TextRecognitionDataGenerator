import cv2
import os
import random
import numpy as np

from PIL import Image, ImageFont, ImageDraw

def create_and_save_sample(index, text, font, out_dir, height, extension, skewing_angle, random_skew):
    image_font = ImageFont.truetype(font=os.path.join('fonts', font), size=32)
    text_width, text_height = image_font.getsize(text)

    txt_img = Image.new('L', (text_width, text_height), 255)
    
    txt_draw = ImageDraw.Draw(txt_img)

    txt_draw.text((0, 0), text, fill=random.randint(1, 80), font=image_font)

    random_angle = random.randint(0-skewing_angle, skewing_angle)

    rotated_img = txt_img.rotate(skewing_angle if not random_skew else random_angle, expand=1)

    new_text_width, new_text_height = rotated_img.size

    # We create our background a bit bigger than the text
    messy_background = create_messy_background(new_text_height + 10, new_text_width + 10)

    mask = rotated_img.point(lambda x: 0 if x == 255 or x == 0 else 255, '1')

    messy_background.paste(rotated_img, (5, 5), mask=mask)

    # Create the name for our image
    image_name = '{}_{}.{}'.format(text, str(index), extension)

    # Resizing the image to desired format
    new_width = float(text_width + 10) * (float(height) / float(text_height + 10))
    final_image = messy_background.resize((int(new_width), height), Image.ANTIALIAS)

    # Save the image
    final_image.convert('RGB').save(os.path.join(out_dir, image_name))

def create_messy_background(height, width):
    """
        Create a background with Gaussian noise (to mimic paper)
    """

    # We create an all white image
    image = np.ones((height, width)) * 255

    # We add gaussian noise
    cv2.randn(image, 235, 10)

    return Image.fromarray(image).convert('L')
