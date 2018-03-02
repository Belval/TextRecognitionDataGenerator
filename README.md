# TextRecognitionDataGenerator [![TravisCI](https://travis-ci.org/Belval/TextRecognitionDataGenerator.svg?branch=master)](https://travis-ci.org/Belval/TextRecognitionDataGenerator) [![codecov](https://codecov.io/gh/Belval/TextRecognitionDataGenerator/branch/master/graph/badge.svg)](https://codecov.io/gh/Belval/TextRecognitionDataGenerator)

A synthetic data generator for text recognition

## What is it for?
Generating text image samples to train an OCR software

## What do I need to make it work?

I use Archlinux so I cannot tell if it works on Windows yet.

```
Python 3.X
OpenCV 3.2 (It probably works with 2.4)
Pillow
Numpy
Requests
BeautifulSoup
```

 You can simply use `pip install -r requirements.txt` too.

## How does it work?
`python run.py -w 5 -f 64`

You get 1000 randomly generated images with random text on them like:

![1](samples/1.jpg "1")
![2](samples/2.jpg "2")
![3](samples/3.jpg "3")
![4](samples/4.jpg "4")
![5](samples/5.jpg "5")

What if you want random skewing? Add `-k` and `-rk` (`python run.py -w 5 -f 64 -k 5 -rk`)

![6](samples/6.jpg "6")
![7](samples/7.jpg "7")
![8](samples/8.jpg "8")
![9](samples/9.jpg "9")
![10](samples/10.jpg "10")

But scanned document usually aren't that clear are they? Add `-bl` and `-rbl` to get gaussian blur on the generated image with user-defined radius (here 0, 1, 2, 4):

![11](samples/11.jpg "0")
![12](samples/12.jpg "1")
![13](samples/13.jpg "2")
![14](samples/14.jpg "4")

Maybe you want another background? Add `-b` to define one of the three available backgrounds: gaussian noise (0), plain white (1), quasicrystal (2) or picture (3).

![15](samples/15.jpg "0")
![16](samples/16.jpg "1")
![17](samples/17.jpg "2")
![23](samples/23.jpg "3")

When using picture background (3). A picture from the pictures/ folder will be randomly selected and the text will be written on it.

Or maybe you are working on an OCR for handwritten text? Add `-hw`! (Experimental)

![18](samples/18.jpg "0")
![19](samples/19.jpg "1")
![20](samples/20.jpg "2")
![21](samples/21.jpg "3")
![22](samples/22.jpg "4")

It uses a Tensorflow model trained using [this excellent project](https://github.com/Grzego/handwriting-generation) by Grzego.

**The project does not require TensorFlow to run if you aren't using this feature**

You can also add distorsion to the generated text with `-d` and `-do`

![23](samples/24.jpg "0")
![24](samples/25.jpg "1")
![25](samples/26.jpg "2")

The text is chosen at random in a dictionary file (that can be found in the *dicts* folder) and drawn on a white background made with Gaussian noise. The resulting image is saved as [text]\_[index].jpg

**New**
- You can add distorsion to the generated text
- You can "fake" handwriting using `-hw`
- You can add gaussian blur to the resulting image
- Sentences from Wikipedia can be used instead of random words with `python run.py -wk 1` (requires an Internet connection)
- Sentences can be picked from a file passed as a parameter with `python run.py -i ./texts/random_1.txt`

There are a lot of parameters that you can tune to get the results you want, therefore I recommand checking out `python run.py -h` for more informations.

## Can I add my own font?

Yes, the script picks a font at random from the *fonts* directory. Simply add / remove fonts until you get the desired output.

It only supports .ttf for now.

## Contributing

1. Create an issue describing the feature you'll be working on
2. Code said feature
3. Create a pull request

## Feature request & issues

If anything is missing, unclear, or simply not working, open an issue on the repository.

## What is left to do?
- Better background generation
- Better handwritten text generation
- More customization parameters (mostly regarding background)
- Implement `--include_symbols`
- Implement `--include_numbers`
