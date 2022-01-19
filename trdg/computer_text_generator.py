import random as rnd

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter


def generate(
    text,
    font,
    text_color,
    font_size,
    orientation,
    space_width,
    character_spacing,
    fit,
    word_split,
    stroke_width=0, 
    stroke_fill="#282828",
):
    if orientation == 0:
        return _generate_horizontal_text(
            text,
            font,
            text_color,
            font_size,
            space_width,
            character_spacing,
            fit,
            word_split,
            stroke_width,
            stroke_fill,
        )
    elif orientation == 1:
        return _generate_vertical_text(
            text, font, text_color, font_size, space_width, character_spacing, fit,
            stroke_width, stroke_fill, 
        )
    else:
        raise ValueError("Unknown orientation " + str(orientation))


def _generate_horizontal_text(
    text, font, text_color, font_size, space_width, character_spacing, fit, word_split, 
    stroke_width=0, stroke_fill="#282828"
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_width = int(image_font.getsize(" ")[0] * space_width)

    if word_split:
        splitted_text = []
        for w in text.split(" "):
            splitted_text.append(w)
            splitted_text.append(" ")
        splitted_text.pop()
    else:
        splitted_text = text

    piece_widths = [
        image_font.getsize(p)[0] if p != " " else space_width for p in splitted_text
    ]
    text_width = sum(piece_widths)
    if not word_split:
        text_width += character_spacing * (len(text) - 1)

    text_height = max([image_font.getsize(p)[1] for p in splitted_text])

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGB", (text_width, text_height), (0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask, mode="RGB")
    txt_mask_draw.fontmode = "1"

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    )

    stroke_colors = [ImageColor.getrgb(c) for c in stroke_fill.split(",")]
    stroke_c1, stroke_c2 = stroke_colors[0], stroke_colors[-1]

    stroke_fill = (
        rnd.randint(min(stroke_c1[0], stroke_c2[0]), max(stroke_c1[0], stroke_c2[0])),
        rnd.randint(min(stroke_c1[1], stroke_c2[1]), max(stroke_c1[1], stroke_c2[1])),
        rnd.randint(min(stroke_c1[2], stroke_c2[2]), max(stroke_c1[2], stroke_c2[2])),
    )

    for i, p in enumerate(splitted_text):
        txt_img_draw.text(
            (sum(piece_widths[0:i]) + i * character_spacing * int(not word_split), 0),
            p,
            fill=fill,
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        txt_mask_draw.text(
            (sum(piece_widths[0:i]) + i * character_spacing * int(not word_split), 0),
            p,
            fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask


def _generate_vertical_text(
    text, font, text_color, font_size, space_width, character_spacing, fit,
    stroke_width=0, stroke_fill="#282828"
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(image_font.getsize(" ")[1] * space_width)

    char_heights = [
        image_font.getsize(c)[1] if c != " " else space_height for c in text
    ]
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights) + character_spacing * len(text)

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask)
    txt_mask_draw.fontmode = "1"

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2]),
    )

    stroke_colors = [ImageColor.getrgb(c) for c in stroke_fill.split(",")]
    stroke_c1, stroke_c2 = stroke_colors[0], stroke_colors[-1] 

    stroke_fill = (
        rnd.randint(stroke_c1[0], stroke_c2[0]),
        rnd.randint(stroke_c1[1], stroke_c2[1]),
        rnd.randint(stroke_c1[2], stroke_c2[2]),
    )

    for i, c in enumerate(text):
        txt_img_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=fill,
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        txt_mask_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask
