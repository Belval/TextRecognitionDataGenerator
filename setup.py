# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="trdg",
    version="1.8.0",
    description="TextRecognitionDataGenerator: A synthetic data generator for text recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Belval/TextRecognitionDataGenerator",
    author="Edouard Belval",
    author_email="edouard@belval.org",
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="synthetic data text-recognition training-set-generator ocr dataset fake text",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    include_package_data=True,
    install_requires=[
        "pillow>=7.0.0",
        "requests>=2.20.0",
        "opencv-python>=4.2.0.32",
        "tqdm>=4.23.0",
        "wikipedia>=1.4.0",
        "diffimg==0.2.3",
        "arabic-reshaper==2.1.3",
        "python-bidi==0.4.2",
    ],
    entry_points={
        "console_scripts": [
            "trdg=trdg.run:main"
        ],
    },
)
