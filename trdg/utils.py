"""
Utility functions
"""

import os


def load_dict(lang):
    """Read the dictionnary file and returns all words in it.
    """

    lang_dict = []
    with open(
        os.path.join(os.path.dirname(__file__), "dicts", lang + ".txt"), "r", encoding="utf8", errors="ignore"
    ) as d:
        lang_dict = [l for l in d.read().splitlines() if len(l) > 0]
    return lang_dict


def load_fonts(folder="fonts/latin"):
    """Load all fonts in the fonts directories
    """
    fonts = []

    if folder is not None:
        for font in os.listdir(os.path.join(os.path.dirname(__file__), folder)):
            if font.split(".")[-1].lower() in ["ttf", "otf"]:
                fonts.append(os.path.join(os.path.dirname(__file__), folder, font))
        return fonts

    raise Exception("No font specified")
