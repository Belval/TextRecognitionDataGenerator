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
Requests
BeautifulSoup
```

 You can simply use `pip install -r requirements.txt` too.

## How does it work?
`python run.py -w 5`

You get 1000 randomly generated images with random text on them like:

![1](samples/1.jpg "1")
![2](samples/2.jpg "2")
![3](samples/3.jpg "3")
![4](samples/4.jpg "4")
![5](samples/5.jpg "5")

You can also add the `-k` and `-rk` (`python run.py -w 5 -k 5 -rk 1`) arguments to add skewing to the generated text like:

![6](samples/6.jpg "6")
![7](samples/7.jpg "7")
![8](samples/8.jpg "8")
![9](samples/9.jpg "9")
![10](samples/10.jpg "10")

The text is chosen at random in a dictionary file (that can be found in the *dicts* folder) and drawn on a white background made with Gaussian noise. The resulting image is saved as [text]_[index].jpg

**New**
- Sentences from Wikipedia can be used instead of random words with `python run.py -wk 1` (requires and Internet connection)
- Sentences can be picked from a file passed as a parameter with `python run.py -i ./lines.txt`

There are a lot of parameters that you can tune to get the results you want, therefore I recommand checking out `python run.py -h` for more informations. 

## Can I add my own font?

Yes, the script picks a font at random from the *fonts* directory. Simply add / remove fonts until you get the desired output.

It only supports .ttf for now.

## Feature request & issues

If anything is missing, unclear, or simply not working, open an issue on the repository.

## What is left to do?
- Better background generation 
- More customization parameters (mostly regarding background)
- Implement `--include_symbols`
- Implemetn `--include_numbers`
