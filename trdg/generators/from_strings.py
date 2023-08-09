import os
from typing import List, Tuple

from trdg.data_generator import FakeTextDataGenerator
from trdg.utils import load_dict, load_fonts

# support RTL
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display


class GeneratorFromStrings:
    """Generator that uses a given list of strings"""

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
        fail_retry_count: int = 5,
        debug = False,
    ):
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
        self.fail_retry_count = fail_retry_count
        self.debug = debug
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.generated_count == self.count:
            raise StopIteration
        self.generated_count += 1
        generated_image = None
        current_string = self.strings[(self.generated_count - 1) % len(self.strings)]
        current_font = self.fonts[(self.generated_count - 1) % len(self.fonts)]
        tries = 0
        while tries < self.fail_retry_count:
            generated_image = FakeTextDataGenerator.generate(
                    self.generated_count,
                    current_string,
                    current_font,
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
                    self.debug
                    )
            if generated_image is not None:
                break
            elif self.debug:
                print (f"Try {tries + 1} to generate image")
            tries += 1
        
        if generated_image is None:
            print (f"Tried {self.fail_retry_count} times to generate image of {current_string}")
            print (f"{current_font} But failed")
        elif generated_image is not None and tries > 1:
            print (f"Tries {tries} times Succeed of {current_string}, {current_font}")
        return (generated_image,
            self.orig_strings[(self.generated_count - 1) % len(self.orig_strings)]
            if self.rtl
            else current_string,
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
