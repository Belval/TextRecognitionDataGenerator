
from trdg.generators import (
    #GeneratorFromDict,
    #GeneratorFromRandom,
    GeneratorFromStrings,
    #GeneratorFromWikipedia,
)

texts = ['تست', 'تست2', 'تست 3']

# The generators use the same arguments as the CLI, only as parameters
generator = GeneratorFromStrings(texts, count=3, blur=2, random_blur=True, language='ar')

for img, lbl in generator:
    # Do something with the pillow images here.
    img.save('tests/out_3/' + lbl + '.png')