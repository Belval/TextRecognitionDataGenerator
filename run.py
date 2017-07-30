import argparse
import os, errno
import random
import re
import requests

from bs4 import BeautifulSoup
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
        "-i",
        "--input-file",
        type=str,
        nargs="?",
        help="When set, this argument uses a specified text file as source for the text",
        default=""
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        nargs="?",
        help="The language to use, should be fr (Français), en (English), es (Español), or de (Deutsch).",
        default="en"
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        nargs="?",        
        help="The number of images to be created.",
        default=1000
    )
    parser.add_argument(
        "-n",
        "--include_numbers",
        type=int,
        nargs="?",        
        help="Define if the text should contain numbers. (NOT IMPLEMENTED)",
        default=1
    )
    parser.add_argument(
        "-s",
        "--include_symbols",
        type=int,
        nargs="?",        
        help="Define if the text should contain symbols. (NOT IMPLEMENTED)",
        default=1
    )
    parser.add_argument(
        "-w",
        "--length",
        type=int,
        nargs="?",        
        help="Define how many words should be included in each generated sample. If the text source is Wikipedia, this is the MINIMUM length",
        default=1
    )
    parser.add_argument(
        "-r",
        "--random",
        type=int,
        nargs="?",
        help="Define if the produced string will have variable word count (with --length being the maximum)",
        default=0
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
        help="Define the number of thread to use for image generation",
        default=1,
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        nargs="?",
        help="Define the extension to save the image with",
        default="jpg",
    )
    parser.add_argument(
        "-k",
        "--skew_angle",
        type=int,
        nargs="?",
        help="Define skewing angle of the generated text. In positive degrees",
        default=0,
    )
    parser.add_argument(
        "-rk",
        "--random_skew",
        type=int,
        nargs="?",
        help="When set to something else than 0, the skew angle will be randomized between the value set with -k and it's opposite",
        default=0,
    )
    parser.add_argument(
        "-wk",
        "--use-wikipedia",
        type=int,
        nargs="?",
        help="Use Wikipedia as the source text for the generation, using this paremeter ignores -r, -n, -s",
        default=0,
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

def create_strings_from_file(filename, count):
    """
        Create all strings by reading lines in specified files
    """

    strings = []

    with open(filename, 'r') as f:
        lines = [l.strip()[0:200] for l in f.readlines()]
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        while len(strings) < count:
            if len(lines) > count - len(strings):
                strings.extend(lines[0:count - len(strings)])                
            else:
                strings.extend(lines)

    return strings

def create_strings_from_dict(length, allow_variable, count, lang_dict):
    """
        Create all strings by picking X random word in the dictionnary
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

def create_strings_from_wikipedia(minimum_length, count, lang):
    """
        Create all string by randomly picking Wikipedia articles and taking sentences from them.
    """
    sentences = []

    while len(sentences) < count:
        # We fetch a random page
        page = requests.get('https://{}.wikipedia.org/wiki/Special:Random'.format(lang))

        soup = BeautifulSoup(page.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract() 

        # Only take a certain length
        lines = list(filter(
            lambda s:
                len(s.split(' ')) > minimum_length
                and not "Wikipedia" in s
                and not "wikipedia" in s,
            [
                ' '.join(re.findall(r"[\w']+", s.strip()))[0:200] for s in soup.get_text().splitlines()
            ]
        ))

        # Remove the last lines that talks about contributing
        sentences.extend(lines[0:max([1, len(lines) - 5])])

    return sentences[0:count]

def main():
    """
        Description: Main function
    """

    # Argument parsing
    args = parse_arguments()

    # Create the directory if it does not exist.
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Creating word list
    lang_dict = load_dict(args.language)

    # Create font (path) list
    fonts = load_fonts()

    # Creating synthetic sentences (or word)
    strings = []
    
    if bool(args.use_wikipedia):
        strings = create_strings_from_wikipedia(args.length, args.count, args.language)
    elif args.input_file != '':
        strings = create_strings_from_file(args.input_file, args.count)
    else:
        strings = create_strings_from_dict(args.length, bool(args.random), args.count, lang_dict)
                

    string_count = len(strings)

    p = Pool(args.thread_count)
    p.starmap(
        create_and_save_sample,
        zip(
            [i for i in range(0, string_count)],
            strings,
            [fonts[random.randrange(0, len(fonts))] for _ in range(0, string_count)],
            [args.output_dir] * string_count,
            [args.format] * string_count,
            [args.extension] * string_count,
            [args.skew_angle] * string_count,
            [args.random_skew] * string_count
        )
    )
    p.terminate()

if __name__ == '__main__':
    main()
