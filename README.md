# TextRecognitionDataGenerator
A synthetic data generator for text recognition

## What is it for?
Generating text image samples to train an OCR

## What do I need to make it work?

I use Archlinux so I cannot tell if it works on Windows yet.

```
Python 3.X
OpenCV 3.2 (It probably works with 2.4)
Pillow
Numpy
```

## How does it work?
`python run.py`

You get 1000 randomly generated images with random text on them like:

![1](samples/1.jpg "1")
![2](samples/2.jpg "2")
![3](samples/3.jpg "3")
![4](samples/4.jpg "4")
![5](samples/5.jpg "5")

The text is chosen at random in a dictionary file (that can be found in the *dicts* folder) and drawn on a white background made with Gaussian noise. The resulting image is saved as [text]_[index].jpg

There are a lot of parameters that you can tune to get the results you want, therefore I recommand checking out `python run.py -h` for more informations. 

## Can I add my own font?

Yes, the script picks a font at random from the *fonts* directory. Simply add / remove fonts until you get the desired output.

It only supports .ttf for now.

## What is left to do?
- Use the `--format` option instead of hard-coded values
- Save as .png or add it as an option
- Support generating skewed text
- Better background generation 
- More customization parameters (mostly regarding background) 
