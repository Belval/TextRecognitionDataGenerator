import os
import random as rnd

import cv2
from PIL import Image, ImageFilter
import numpy as np
import computer_text_generator
import background_generator
import distorsion_generator
from skimage import img_as_ubyte

from skimage.filters import threshold_sauvola#, threshold_adaptive

import imgaug as ia
import imgaug.augmenters as iaa

try:
    import handwritten_text_generator
except ImportError as e:
    print('Missing modules for handwritten text generation.')


class FakeTextDataGenerator(object):
    sometimes = lambda aug: iaa.Sometimes(0.5, aug)
    seq = iaa.Sequential([
            sometimes(iaa.PerspectiveTransform(scale=(0.01, 0.08))),
            sometimes(
                iaa.OneOf([
                    iaa.CoarseDropout((0.03, 0.05), size_percent=(0.1, 0.3)),
                    iaa.CoarseDropout((0.03, 0.1), size_percent=(0.1, 0.3), per_channel=1.0),
                    iaa.Dropout((0.03,0.1)),
                    iaa.Salt((0.03,0.1))
                ])
            ),
            iaa.Multiply((0.3, 1.7), per_channel=0.5),
            sometimes(iaa.AdditiveGaussianNoise((0.02, 0.2))),
            sometimes(
                iaa.OneOf([
                    iaa.MotionBlur(k=(3,5),angle=(0, 360)),
                    iaa.GaussianBlur((0, 1.3)),
                    iaa.AverageBlur(k=(2, 4)),
                    iaa.MedianBlur(k=(3, 7))
                ])
            ),
            sometimes(
                iaa.CropAndPad(
                    percent=(-0.05, 0.15),
                    pad_mode=ia.ALL,
                    pad_cval=(0, 255)
                ),
            ),
            sometimes(iaa.Add((-50, 50), per_channel=0.5)),
            sometimes(iaa.AdditivePoissonNoise((0.02,0.1))),
            sometimes(iaa.ElasticTransformation(alpha=(1.0, 2.0), sigma=(2.0, 3.0))), # move pixels locally around (with random strengths)
            sometimes(iaa.PiecewiseAffine(scale=(0.01, 0.02))), # sometimes move parts of the image around
            sometimes(iaa.FrequencyNoiseAlpha(
                    exponent=(-4, 0),
                    first=iaa.Multiply((0.8, 1.2), per_channel=0.5),
                    second=iaa.ContrastNormalization((0.5, 3.0))
                )
            ),
        ]
    )

    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @classmethod
    def generate(cls, index, text, font, out_dir, size, extension, skewing_angle, random_skew, blur, random_blur, background_type, distorsion_type, distorsion_orientation, is_handwritten, name_format, width, alignment, text_color, orientation, space_width, margins, fit, imgaug1, treshold):
        image = None

        margin_top, margin_left, margin_bottom, margin_right = margins
        horizontal_margin = margin_left + margin_right
        vertical_margin = margin_top + margin_bottom

        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            if orientation == 1:
                raise ValueError("Vertical handwritten text is unavailable")
            image = handwritten_text_generator.generate(text, text_color)
        else:
            image = computer_text_generator.generate(text, font, text_color, size, orientation, space_width, fit)

        random_angle = rnd.randint(0-skewing_angle, skewing_angle)

        rotated_img = image.rotate(skewing_angle if not random_skew else random_angle, expand=1)

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img # Mind = blown
        elif distorsion_type == 1:
            distorted_img = distorsion_generator.sin(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )
        elif distorsion_type == 2:
            distorted_img = distorsion_generator.cos(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )
        else:
            distorted_img = distorsion_generator.random(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )

        ##################################
        # Resize image to desired format #
        ##################################

        # Horizontal text
        if orientation == 0:
            new_width = int(distorted_img.size[0] * (float(size - vertical_margin) / float(distorted_img.size[1])))
            resized_img = distorted_img.resize((new_width, size - vertical_margin), Image.ANTIALIAS)
            background_width = width if width > 0 else new_width + horizontal_margin
            background_height = size
        # Vertical text
        elif orientation == 1:
            new_height = int(float(distorted_img.size[1]) * (float(size - horizontal_margin) / float(distorted_img.size[0])))
            resized_img = distorted_img.resize((size - horizontal_margin, new_height), Image.ANTIALIAS)
            background_width = size
            background_height = new_height + vertical_margin
        else:
            raise ValueError("Invalid orientation")

        #############################
        # Generate background image #
        #############################
        if background_type == 0:
            background = background_generator.gaussian_noise(background_height, background_width)
        elif background_type == 1:
            background = background_generator.plain_white(background_height, background_width)
        elif background_type == 2:
            background = background_generator.quasicrystal(background_height, background_width)
        elif background_type == 3:
            background_func= rnd.choice([background_generator.plain_white, background_generator.gaussian_noise])
            background = background_func(background_height, background_width)
        else:
            background = background_generator.picture(background_height, background_width)

        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size

        if alignment == 0 or width == -1:
            background.paste(resized_img, (margin_left, margin_top), resized_img)
        elif alignment == 1:
            background.paste(resized_img, (int(background_width / 2 - new_text_width / 2), margin_top), resized_img)
        else:
            background.paste(resized_img, (background_width - new_text_width - margin_right, margin_top), resized_img)

        ##################################
        # Apply Image augmentation #
        ##################################
        if imgaug1:
            background = np.array(background)
            image = cls.seq.augment_images([background])[0]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            background = Image.fromarray(img_as_ubyte(image))

        ##################################
        # Apply sauvola method #
        ##################################
        if treshold and rnd.random() < 0.3:
            background = np.array(background)
            thresh_sauvola = threshold_sauvola(background, window_size=rnd.choice([17,25]))
            background = Image.fromarray(img_as_ubyte(background > thresh_sauvola))

        ##################################
        # Apply gaussian blur #
        ##################################
        final_image = background.filter(
            ImageFilter.GaussianBlur(
                radius=(blur if not random_blur else rnd.randint(0, blur))
            )
        )

        #####################################
        # Generate name for resulting image #
        #####################################
        if name_format == 0:
            image_name = '{}_{}.{}'.format(text, str(index), extension)
        elif name_format == 1:
            image_name = '{}_{}.{}'.format(str(index), text, extension)
        elif name_format == 2:
            image_name = '{}.{}'.format(str(index),extension)
        else:
            print('{} is not a valid name format. Using default.'.format(name_format))
            image_name = '{}_{}.{}'.format(text, str(index), extension)

        # Save the image
        final_image.convert('RGB').save(os.path.join(out_dir, image_name))
