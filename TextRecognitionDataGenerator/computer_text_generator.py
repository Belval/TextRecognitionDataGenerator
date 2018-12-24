import random

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter

class ComputerTextGenerator(object):
    @classmethod
    def generate(cls, text, font, text_color, font_size, orientation, space_width):
        if orientation == 0:
            return cls.__generate_horizontal_text(text, font, text_color, font_size, space_width)
        elif orientation == 1:
            return cls.__generate_vertical_text(text, font, text_color, font_size, space_width)
        else:
            raise ValueError("Unknown orientation " + str(orientation))
    
    @classmethod
    def __generate_horizontal_text(cls, text, font, text_color, font_size, space_width):
        image_font = ImageFont.truetype(font=font, size=font_size)
        words = text.split(' ')
        space_width = image_font.getsize(' ')[0] * space_width

        words_width = [image_font.getsize(w)[0] for w in words]
        text_width =  sum(words_width) + int(space_width) * (len(words) - 1)
        text_height = max([image_font.getsize(w)[1] for w in words])

        txt_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))

        txt_draw = ImageDraw.Draw(txt_img)

        colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
        c1, c2 = colors[0], colors[-1]

        fill = (
            random.randint(c1[0], c2[0]),
            random.randint(c1[1], c2[1]),
            random.randint(c1[2], c2[2])
        )

        for i, w in enumerate(words):
            txt_draw.text((sum(words_width[0:i]) + i * int(space_width), 0), w, fill=fill, font=image_font)

        return txt_img

    @classmethod
    def __generate_vertical_text(cls, text, font, text_color, font_size, space_width):
        image_font = ImageFont.truetype(font=font, size=font_size)
        
        space_height = int(image_font.getsize(' ')[1] * space_width)

        char_heights = [image_font.getsize(c)[1] if c != ' ' else space_height for c in text]
        text_width = max([image_font.getsize(c)[0] for c in text])
        text_height = sum(char_heights)

        txt_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))

        txt_draw = ImageDraw.Draw(txt_img)

        colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
        c1, c2 = colors[0], colors[-1]

        fill = (
            random.randint(c1[0], c2[0]),
            random.randint(c1[1], c2[1]),
            random.randint(c1[2], c2[2])
        )

        for i, c in enumerate(text):
            txt_draw.text((0, sum(char_heights[0:i])), c, fill=fill, font=image_font)

        return txt_img
