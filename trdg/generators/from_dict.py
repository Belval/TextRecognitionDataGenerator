import os
from typing import List, Tuple

from trdg.generators.from_strings import GeneratorFromStrings
from trdg.data_generator import FakeTextDataGenerator
from trdg.string_generator import create_strings_from_dict
from trdg.utils import load_dict, load_fonts


class GeneratorFromDict:
    def __init__(
        self,
        count: int = -1,
        length: int = 1,
        allow_variable: bool = False,
        fonts: List[str] = [],
        language: str = "en",
        size: int = 32,
        skewing_angle: int = 0,
        random_skew: bool = False,
        blur: int = 0,
        random_blur: bool = False,
        background_type: int = 0,
        distorsion_type: int = 0,
        distorsion_orientation: int = 0,
        is_handwritten: bool = False,
        width: int = -1,
        alignment: int = 1,
        text_color: str = "#282828",
        orientation: int = 0,
        space_width: float = 1.0,
        character_spacing: int = 0,
        margins: Tuple[int, int, int, int] = (5, 5, 5, 5),
        fit: bool = False,
        output_mask: bool = False,
        word_split: bool = False,
        image_dir: str = os.path.join(
            "..", os.path.split(os.path.realpath(__file__))[0], "images"
        ),
        stroke_width: int = 0,
        stroke_fill: str = "#282828",
        image_mode: str = "RGB",
        output_bboxes: int = 0,
        path: str = "",
        rtl: bool = False,
    ):
        """Generator that uses words taken from pre-packaged dictionaries

        :param count: Number of samples to pre-generate, defaults to -1
        :type count: int, optional
        :param length: Number of words in the generated crop, defaults to 1
        :type length: int, optional
        :param allow_variable: Allow a variable number of words in the crop, defaults to False
        :type allow_variable: bool, optional
        :param fonts: List of font paths, defaults to []
        :type fonts: List[str], optional
        :param language: Language ISO code, defaults to "en"
        :type language: str, optional
        :param size: Text crop height (if horizontal) or width (if vertical), defaults to 32
        :type size: int, optional
        :param skewing_angle: Rotate the generated text, defaults to 0
        :type skewing_angle: int, optional
        :param random_skew: Rotate the generated text by a random value in [-skewing_angle, skewing_angle], defaults to False
        :type random_skew: bool, optional
        :param blur: Blur the generated text, defaults to 0
        :type blur: int, optional
        :param random_blur: Blur the generated text by a random value in [-blur, blur], defaults to False
        :type random_blur: bool, optional
        :param background_type: 0: Gaussian Noise, 1: Plain white, 2: Quasicrystal, 3: Image, defaults to 0
        :type background_type: int, optional
        :param distorsion_type: 0: None (Default), 1: Sine wave, 2: Cosine wave, 3: Random, defaults to 0
        :type distorsion_type: int, optional
        :param distorsion_orientation: 0: Vertical (Up and down), 1: Horizontal (Left and Right), 2: Both, defaults to 0
        :type distorsion_orientation: int, optional
        :param is_handwritten: Generate handwritten crops using an RNN, defaults to False
        :type is_handwritten: bool, optional
        :param width: Width of the resulting crop, defaults to -1
        :type width: int, optional
        :param alignment: 0: left, 1: center, 2: right. Only used if the width parameter is set, defaults to 1
        :type alignment: int, optional
        :param text_color: Text color, should be either a single hex color or a range in the ?,?, defaults to "#282828"
        :type text_color: str, optional
        :param orientation: Orientation of the text. 0: Horizontal, 1: Vertical, defaults to 0
        :type orientation: int, optional
        :param space_width: Width of the spaces between words. 2.0 means twice the normal space width, defaults to 1.0
        :type space_width: float, optional
        :param character_spacing: Width of the spaces between characters. 2 means two pixels, defaults to 0
        :type character_spacing: int, optional
        :param margins: Margins around the text when rendered. In pixels, defaults to (5, 5, 5, 5)
        :type margins: Tuple[int, int, int, int], optional
        :param fit: Apply a tight crop around the rendered text, defaults to False
        :type fit: bool, optional
        :param output_mask: Define if the generator will return masks for the text, defaults to False
        :type output_mask: bool, optional
        :param word_split: Split on words instead of on characters (preserves ligatures, no character spacing), defaults to False
        :type word_split: bool, optional
        :param image_dir: Image directory to use when background is set to image, defaults to os.path.join( "..", os.path.split(os.path.realpath(__file__))[0], "images" )
        :type image_dir: str, optional
        :param stroke_width: Width of the text strokes, defaults to 0
        :type stroke_width: int, optional
        :param stroke_fill: Color of the contour of the strokes, if stroke_width is bigger than 0, defaults to "#282828"
        :type stroke_fill: str, optional
        :param image_mode: Image mode to be used. RGB is default, L means 8-bit grayscale images, 1 means 1-bit binary images stored with one pixel per byte, defaults to "RGB"
        :type image_mode: str, optional
        :param output_bboxes: Define if the generator will return bounding boxes for the text, 1: Bounding box file, 2: Tesseract format, defaults to 0
        :type output_bboxes: int, optional
        :param path: Dictionary path, defaults to ""
        :type path: str, optional
        :param rtl: Right to left, set this to true for RTL languages, defaults to False
        :type rtl: bool, optional
        """                
        self.count = count
        self.length = length
        self.allow_variable = allow_variable

        if path == "":
            self.dict = load_dict(
                os.path.join(
                    os.path.dirname(__file__), "..", "dicts", language + ".txt"
                )
            )
        else:
            self.dict = load_dict(path)

        self.batch_size = min(max(count, 1), 1000)
        self.steps_until_regeneration = self.batch_size

        self.generator = GeneratorFromStrings(
            create_strings_from_dict(
                self.length, self.allow_variable, self.batch_size, self.dict
            ),
            count,
            fonts if len(fonts) else load_fonts(language),
            language,
            size,
            skewing_angle,
            random_skew,
            blur,
            random_blur,
            background_type,
            distorsion_type,
            distorsion_orientation,
            is_handwritten,
            width,
            alignment,
            text_color,
            orientation,
            space_width,
            character_spacing,
            margins,
            fit,
            output_mask,
            word_split,
            image_dir,
            stroke_width,
            stroke_fill,
            image_mode,
            output_bboxes,
            rtl,
        )

    def __iter__(self):
        return self.generator

    def __next__(self):
        return self.next()

    def next(self):
        if self.generator.generated_count >= self.steps_until_regeneration:
            self.generator.strings = create_strings_from_dict(
                self.length, self.allow_variable, self.batch_size, self.dict
            )
            self.steps_until_regeneration += self.batch_size
        return self.generator.next()
