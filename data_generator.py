import os
import cv2
import random

from PIL import Image, ImageFilter

from computer_text_generator import ComputerTextGenerator
from handwritten_text_generator import HandwrittenTextGenerator
from background_generator import BackgroundGenerator

class FakeTextDataGenerator(object):
    @classmethod
    def generate(cls, index, text, font, out_dir, height, extension, skewing_angle, random_skew, blur, random_blur, background_type, is_handwritten):
        image = None

        if is_handwritten:
            image = HandwrittenTextGenerator.generate(text)
        else:
            image = ComputerTextGenerator.generate(text, font)

        random_angle = random.randint(0-skewing_angle, skewing_angle)

        # Somehow the handwritten text always has a little bit of angle.
        # this fixes it.
        if is_handwritten:
            random_angle -= 8
            skewing_angle -= 8

        rotated_img = image.rotate(skewing_angle if not random_skew else random_angle, expand=1)

        new_text_width, new_text_height = rotated_img.size

        # We create our background a bit bigger than the text
        background = None

        if background_type == 0:
            background = BackgroundGenerator.gaussian_noise(new_text_height + 10, new_text_width + 10)
        elif background_type == 1:
            background = BackgroundGenerator.plain_white(new_text_height + 10, new_text_width + 10)
        else:
            background = BackgroundGenerator.quasicrystal(new_text_height + 10, new_text_width + 10)

        mask = rotated_img.point(lambda x: 0 if x == 255 or x == 0 else 255, '1')

        background.paste(rotated_img, (5, 5), mask=mask)

        # Create the name for our image
        image_name = '{}_{}.{}'.format(text, str(index), extension)

        # Resizing the image to desired format
        new_width = float(new_text_width + 10) * (float(height) / float(new_text_height + 10))
        image_on_background = background.resize((int(new_text_width), height), Image.ANTIALIAS)

        final_image = image_on_background.filter(
            ImageFilter.GaussianBlur(
                radius=(blur if not random_blur else random.randint(0, blur))
            )
        )

        # Save the image
        final_image.convert('RGB').save(os.path.join(out_dir, image_name))
