import os
from typing import List, Tuple

from trdg.data_generator import FakeTextDataGenerator
from trdg.utils import load_dict, load_fonts

# support RTL
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display


class GeneratorFromStrings:
    def __init__(
        self,
        strings: List[str],
        count: int = -1,
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
        rtl: bool = False,
    ):
        """Generator that uses words from a list of strings

        :param strings: List of strings to use 
        :type strings: List[str]
        :param count: Number of samples to pre-generate, defaults to -1
        :type count: int, optional
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
        :param rtl: Right to left, set this to true for RTL languages, defaults to False
        :type rtl: bool, optional
        """    
        self.count = count
        self.strings = strings
        self.fonts = fonts
        if len(fonts) == 0:
            self.fonts = load_fonts(language)
        self.rtl = rtl
        self.orig_strings = []
        if self.rtl:
            if language == "ckb":
                ar_reshaper_config = {"delete_harakat": True, "language": "Kurdish"}
            else:
                ar_reshaper_config = {"delete_harakat": False}
            self.rtl_shaper = ArabicReshaper(configuration=ar_reshaper_config)
            # save a backup of the original strings before arabic-reshaping
            self.orig_strings = self.strings
            # reshape the strings
            self.strings = self.reshape_rtl(self.strings, self.rtl_shaper)
        self.language = language
        self.size = size
        self.skewing_angle = skewing_angle
        self.random_skew = random_skew
        self.blur = blur
        self.random_blur = random_blur
        self.background_type = background_type
        self.distorsion_type = distorsion_type
        self.distorsion_orientation = distorsion_orientation
        self.is_handwritten = is_handwritten
        self.width = width
        self.alignment = alignment
        self.text_color = text_color
        self.orientation = orientation
        self.space_width = space_width
        self.character_spacing = character_spacing
        self.margins = margins
        self.fit = fit
        self.output_mask = output_mask
        self.word_split = word_split
        self.image_dir = image_dir
        self.output_bboxes = output_bboxes
        self.generated_count = 0
        self.stroke_width = stroke_width
        self.stroke_fill = stroke_fill
        self.image_mode = image_mode

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.generated_count == self.count:
            raise StopIteration
        self.generated_count += 1
        return (
            FakeTextDataGenerator.generate(
                self.generated_count,
                self.strings[(self.generated_count - 1) % len(self.strings)],
                self.fonts[(self.generated_count - 1) % len(self.fonts)],
                None,
                self.size,
                None,
                self.skewing_angle,
                self.random_skew,
                self.blur,
                self.random_blur,
                self.background_type,
                self.distorsion_type,
                self.distorsion_orientation,
                self.is_handwritten,
                0,
                self.width,
                self.alignment,
                self.text_color,
                self.orientation,
                self.space_width,
                self.character_spacing,
                self.margins,
                self.fit,
                self.output_mask,
                self.word_split,
                self.image_dir,
                self.stroke_width,
                self.stroke_fill,
                self.image_mode,
                self.output_bboxes,
            ),
            self.orig_strings[(self.generated_count - 1) % len(self.orig_strings)]
            if self.rtl
            else self.strings[(self.generated_count - 1) % len(self.strings)],
        )

    def reshape_rtl(self, strings: list, rtl_shaper: ArabicReshaper):
        # reshape RTL characters before generating any image
        rtl_strings = []
        for string in strings:
            reshaped_string = rtl_shaper.reshape(string)
            rtl_strings.append(get_display(reshaped_string))
        return rtl_strings


if __name__ == "__main__":
    from trdg.generators.from_wikipedia import GeneratorFromWikipedia

    s = GeneratorFromWikipedia("test")
    next(s)
