import argparse
import os
import random

from PIL import Image, ImageFont
from generator import create_and_save_sample
from multiprocessing import Pool

def parse_arguments():
    """
        Parse the command line arguments of the program.
    """
    
    parser = argparse.ArgumentParser(description='Generate synthetic text data for text recognition.')
    parser.add_argument(
        "output_dir",
        type=str,
        nargs="?",
        help="The output directory",
        default="out/",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        nargs="?",
        help="The language to use, should be fra (Français), eng (English), esp (Español), or deu (Deutsch).",
        default="eng"
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        nargs="?",        
        help="Define the language to be used to data generation.",
        default=1000
    )
    parser.add_argument(
        "-n",
        "--include_numbers",
        type=int,
        nargs="?",        
        help="Define if the text should contain numbers.",
        default=1
    )
    parser.add_argument(
        "-s",
        "--include_symbols",
        type=int,
        nargs="?",        
        help="Define if the text should contain symbols.",
        default=1
    )
    parser.add_argument(
        "-w",
        "--length",
        type=int,
        nargs="?",        
        help="Define how many words should be included in each generated sample.",
        default=1
    )
    parser.add_argument(
        "-r",
        "--random",
        type=int,
        nargs="?",
        help="Define if the produced string will have variable word count (with --length being the maximum)",
        default=1
    )
    parser.add_argument(
        "-f",
        "--format",
        type=int,
        nargs="?",
        help="Define the height of the produced images",
        default=32,
    )
    parser.add_argument(
        "-t",
        "--thread_count",
        type=int,
        nargs="?",
        help="Define the number of thread to use for image generation"
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        nargs="?",
        help="Define the extension to save the image with",
        default="jpg",
    )
    return parser.parse_args()

def load_dict(lang):
    """
        Read the dictionnary file and returns all words in it.
    """

    lang_dict = []
    with open(os.path.join('dicts', lang + '.txt'), 'r') as d:
        lang_dict = d.readlines()
    return lang_dict

def load_fonts():
    """
        Load all fonts in the fonts directory
    """

    return [font for font in os.listdir('fonts')]

def create_strings(length, allow_variable, count, lang_dict):
    """
        Create a string by picking X random word in the dictionnary
    """

    dict_len = len(lang_dict)
    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, random.randint(1, length) if allow_variable else length):
            current_string += lang_dict[random.randrange(dict_len)][:-1]
            current_string += ' '
        strings.append(current_string[:-1])
    return strings

def main():
    """
        Description: Main function
    """

    # Argument parsing
    args = parse_arguments()

    # Creating word list
    lang_dict = load_dict(args.language)

    # Create font (path) list
    fonts = load_fonts()

    # Creating synthetic sentences (or word)
    strings = create_strings(args.length, bool(args.random), args.count, lang_dict)

    p = Pool(args.thread_count)
    p.starmap(
        create_and_save_sample,
        zip(
            [i for i in range(0, len(strings))],
            strings,
            [fonts[random.randrange(0, len(fonts))] for _ in range(0, len(strings))],
            [args.output_dir] * len(strings),
            [args.format] * len(strings),
            [args.extension] * len(strings),
        )
    )
    p.terminate()

if __name__ == '__main__':
    main()
