import os

from trdg.data_generator import FakeTextDataGenerator
from trdg.utils import load_dict, load_fonts

# support RTL
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display

class GeneratorFromStrings:
    """Generator that uses a given list of strings"""

    def __init__(
        self,
        strings,
        count=-1,
        fonts=[],
        language="en",
        size=32,
        skewing_angle=0,
        random_skew=False,
        blur=0,
        random_blur=False,
        background_type=0,
        distorsion_type=0,
        distorsion_orientation=0,
        is_handwritten=False,
        width=-1,
        alignment=1,
        text_color="#282828",
        orientation=0,
        space_width=1.0,
        character_spacing=0,
        margins=(5, 5, 5, 5),
        fit=False,
        output_mask=False,
        word_split=False,
        image_dir=os.path.join(
            "..", os.path.split(os.path.realpath(__file__))[0], "images"
        ),
        stroke_width=0, 
        stroke_fill="#282828",
        image_mode="RGB",
        output_bboxes=0,
        rtl=False,
    ):
        self.count = count
        self.strings = strings
        self.fonts = fonts
        if len(fonts) == 0:
            self.fonts = load_fonts(language)
        self.rtl = rtl
        self.orig_strings = []
        if self.rtl:
            self.rtl_shaper = ArabicReshaper(configuration={"delete_harakat":False})
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
            self.orig_strings[(self.generated_count - 1) % len(self.orig_strings)] if self.rtl else self.strings[(self.generated_count - 1) % len(self.strings)],
        )

    def reshape_rtl(self, strings: list, rtl_shaper: ArabicReshaper):
        # reshape RTL characters before generating any image
        rtl_strings = []
        for string in strings:
            reshaped_string = rtl_shaper.reshape(string)
            rtl_strings.append(get_display(reshaped_string))
        return rtl_strings

if __name__ == '__main__':
    from trdg.generators.from_wikipedia import GeneratorFromWikipedia
    s = GeneratorFromWikipedia("test")
    next(s)
