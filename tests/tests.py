import os
import sys
import unittest
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    os.mkdir('tests/out')
except:
    pass

from TextRecognitionDataGenerator.data_generator import FakeTextDataGenerator
from TextRecognitionDataGenerator.background_generator import BackgroundGenerator
from TextRecognitionDataGenerator.run import (
    create_strings_from_file,
    create_strings_from_dict,
    create_strings_from_wikipedia
)

def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        hash_md5.update(f.read())
    h = hash_md5.hexdigest()
    return h

class DataGenerator(unittest.TestCase):
    def test_create_string_from_wikipedia(self):
        """
            Test that the function returns different output if called twice.
            (And that it doesn't throw of course)
        """

        strings = create_strings_from_wikipedia(20, 2, 'en')

        self.assertTrue(
            len(strings) == 2 and
            strings[0] != strings[1] and
            len(strings[0].split(' ')) >= 20 and
            len(strings[1].split(' ')) >= 20
        )

    def test_create_string_from_file(self):
        strings = create_strings_from_file('tests/test.txt', 6)

        self.assertTrue(
            len(strings) == 6 and
            strings[0] != strings[1] and
            strings[0] == strings[3]
        )

    def test_create_strings_from_dict(self):
        strings = create_strings_from_dict(3, False, 2, ['TEST\n', 'TEST\n', 'TEST\n', 'TEST\n'])

        self.assertTrue(
            len(strings) == 2 and
            len(strings[0].split(' ')) == 3
        )

    def test_generate_data_with_format(self):
        FakeTextDataGenerator.generate(
            0,
            'TEST TEST TEST',
            'tests/font.ttf',
            'tests/out/',
            64,
            'jpg',
            0,
            False,
            0,
            False,
            1,
            False,
            1
        )

        self.assertTrue(
            md5('tests/out/TEST TEST TEST_0.jpg') == md5('tests/expected_results/TEST TEST TEST_0.jpg')
        )

        os.remove('tests/out/TEST TEST TEST_0.jpg')

    def test_generate_data_with_extension(self):
        FakeTextDataGenerator.generate(
            1,
            'TEST TEST TEST',
            'tests/font.ttf',
            'tests/out/',
            32,
            'png',
            0,
            False,
            0,
            False,
            1,
            False,
            1
        )

        self.assertTrue(
            md5('tests/out/TEST TEST TEST_1.png') == md5('tests/expected_results/TEST TEST TEST_1.png')
        )

        os.remove('tests/out/TEST TEST TEST_1.png')

    def test_generate_data_with_skew_angle(self):
        FakeTextDataGenerator.generate(
            2,
            'TEST TEST TEST',
            'tests/font.ttf',
            'tests/out/',
            64,
            'jpg',
            15,
            False,
            0,
            False,
            1,
            False,
            1
        )

        self.assertTrue(
            md5('tests/out/TEST TEST TEST_2.jpg') == md5('tests/expected_results/TEST TEST TEST_2.jpg')
        )

        os.remove('tests/out/TEST TEST TEST_2.jpg')

    def test_generate_data_with_blur(self):
        FakeTextDataGenerator.generate(
            3,
            'TEST TEST TEST',
            'tests/font.ttf',
            'tests/out/',
            64,
            'jpg',
            0,
            False,
            3,
            False,
            1,
            False,
            1
        )

        self.assertTrue(
            md5('tests/out/TEST TEST TEST_3.jpg') == md5('tests/expected_results/TEST TEST TEST_3.jpg')
        )

        os.remove('tests/out/TEST TEST TEST_3.jpg')

    def test_generate_data_with_white_background(self):
        BackgroundGenerator.plain_white(64, 128).save('tests/out/white_background.jpg')

        self.assertTrue(
            md5('tests/out/white_background.jpg') == md5('tests/expected_results/white_background.jpg')
        )

        os.remove('tests/out/white_background.jpg')

    def test_generate_data_with_gaussian_background(self):
        BackgroundGenerator.gaussian_noise(64, 128).save('tests/out/gaussian_background.jpg')

        self.assertTrue(
            md5('tests/out/gaussian_background.jpg') == md5('tests/expected_results/gaussian_background.jpg')
        )

        os.remove('tests/out/gaussian_background.jpg')

if __name__=='__main__':
    unittest.main()
