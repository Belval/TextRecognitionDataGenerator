import os
import random as rnd

from PIL import Image, ImageFilter, ImageStat
from PIL import ImageFont, ImageDraw

from trdg import computer_text_generator, background_generator, distorsion_generator, object_generator
from trdg.utils import mask_to_bboxes

try:
    from trdg import handwritten_text_generator
except ImportError as e:
    print("Missing modules for handwritten text generation.")


class FakeObjectDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """
        cls.generate(*t)

    @classmethod
    def generate(
        cls,
        index,
        strings,
        name,
        output_image_width,
        output_image_height,
        object_width,
        skewing_angle,
        random_skew,
        blur,
        random_blur,
        background,
        distorsion_type,
        distorsion_orientation,
        background_type,
        name_format,
        out_dir,
    ):
        image = None
        print(strings)
        OUTPUT_IMAGE_WIDTH = output_image_width
        OUTPUT_IMAGE_HEIGHT = output_image_height
        image_dir = "images"
        OUTPUT_FILE_NAME=name
        OBJECT_WIDTH=object_width


        #margin_top, margin_left, margin_bottom, margin_right = margins
        #horizontal_margin = margin_left + margin_right
        #vertical_margin = margin_top + margin_bottom

        ##########################
        # Create picture of text #
        ##########################
        if os.path.exists(strings):
            image, mask = object_generator.generate(
                strings)
        else:
            image = Image.new(
                "RGB", (object_width, object_width*3), (255, 255, 255, 0)
            )
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(r'/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf', 32)
            draw.text((10, 20), strings, font=font, fill=(100, 100 , 100, 255))
            mask = image


        """
        random_angle = rnd.randint(0 - skewing_angle, skewing_angle)

        rotated_img = image.rotate(
            skewing_angle if not random_skew else random_angle, expand=1
        )

        rotated_mask = mask.rotate(
            skewing_angle if not random_skew else random_angle, expand=1
        )
            """

        random_angle = rnd.randint(0 - skewing_angle, skewing_angle)
        image = image.convert('RGBA')
        rotated_img = image.rotate(
            skewing_angle if not random_skew else random_angle, expand=1, fillcolor = (255,255,255,0)
        )

        rotated_mask = mask.rotate(
            skewing_angle if not random_skew else random_angle, expand=1
        )

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img  # Mind = blown
            distorted_mask = rotated_mask
        elif distorsion_type == 1:
            distorted_img, distorted_mask = distorsion_generator.sin(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
        elif distorsion_type == 2:
            distorted_img, distorted_mask = distorsion_generator.cos(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
        else:
            distorted_img, distorted_mask = distorsion_generator.random(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )

        ##################################
        # Resize image to desired format #
        ##################################

        # Horizontal text
        size=OBJECT_WIDTH
        horizontal_margin = 0
        vertical_margin = 0

        new_width = int(
                distorted_img.size[0]
                * (float(size - vertical_margin) / float(distorted_img.size[1]))
        )
        resized_img = distorted_img.resize(
                (new_width, size - vertical_margin), Image.ANTIALIAS
        )
        resized_mask = distorted_mask.resize((new_width, size - vertical_margin), Image.NEAREST)

        #############################
        # Generate background image #
        #############################
        background_width = OUTPUT_IMAGE_WIDTH
        background_height = OUTPUT_IMAGE_HEIGHT

        if background_type >= 100:
            background_type = rnd.randint(0, 3)

        if background_type == 0:
            background_img = background_generator.gaussian_noise(
                background_height, background_width
            )
        elif background_type == 1:
            background_img = background_generator.plain_white(
                background_height, background_width
            )
        elif background_type == 2:
            background_img = background_generator.quasicrystal(
                background_height, background_width
            )
        else:
            background_img = background_generator.image(
                background_height, background_width, image_dir
            )
        background_mask = Image.new(
            "RGB", (background_width, background_height), (0, 0, 0)
        )

        ##############################################################
        # Comparing average pixel value of text and background image #
        ##############################################################
        try:
            background_mask = background_img
            resized_mask = resized_img
            resized_img_st = ImageStat.Stat(resized_img, resized_mask.split()[2])
            background_img_st = ImageStat.Stat(background_img)
            resized_img_px_mean = sum(resized_img_st.mean[:2]) / 3
            background_img_px_mean = sum(background_img_st.mean) / 3
            if abs(resized_img_px_mean - background_img_px_mean) < 15:
                print("value of mean pixel is too similar. Ignore this image")
                print("resized_img_st \n {}".format(resized_img_st.mean))
                print("background_img_st \n {}".format(background_img_st.mean))

                return
        except Exception as err:
            print("Cannot compute image stats")
            print(err)
            return

        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size
        width=-10
        alignment=3
        if alignment == 0 or width == -1:
            background_img.paste(resized_img, (margin_left, margin_top), resized_img)
            background_mask.paste(resized_mask, (margin_left, margin_top))
        elif alignment == 1:
            background_img.paste(
                resized_img,
                (int(background_width / 2 - new_text_width / 2), margin_top),
                resized_img,
            )
            background_mask.paste(
                resized_mask,
                (int(background_width / 2 - new_text_width / 2), margin_top),
            )
        else:
            print(" bg.x: {}, object.x: {}".format(background_img.size[0], resized_img.size[0] ))
            if resized_img.size[0] > background_img.size[0]:
                object_offset_x = 0
            else:
                object_offset_x = rnd.randint(0,background_img.size[0] - resized_img.size[0] )
            if resized_img.size[1] > background_img.size[1]:
                object_offset_y = 0
            else:
                object_offset_y = rnd.randint(0, background_img.size[1] - resized_img.size[1])
            background_img.paste(
                resized_img.copy(),
                ((object_offset_x , object_offset_y)),
                resized_img.convert("RGBA"),
            )

        #######################
        # Apply gaussian blur #
        #######################
        gaussian_filter = ImageFilter.GaussianBlur(
            radius=blur if not random_blur else rnd.randint(0, blur)
        )
        final_image = background_img.filter(gaussian_filter)
        final_mask = background_mask.filter(gaussian_filter)
        
        ############################################
        # Change image mode (RGB, grayscale, etc.) #
        ############################################
        image_mode="RGB"
        final_image = final_image.convert(image_mode)
        final_mask = final_mask.convert(image_mode) 

        #####################################
        # Generate name for resulting image #
        #####################################
        # We remove spaces if space_width == 0
        space_width = 0
        text=OUTPUT_FILE_NAME
        if space_width == 0:
            text = text.replace(" ", "")
        if name_format == 0:
            name = "{}_{}".format(text, str(index))
        elif name_format == 1:
            name = "{}_{}".format(str(index), text)
        elif name_format == 2:
            name = str(index)
        else:
            print("{} is not a valid name format. Using default.".format(name_format))
            name = "{}_{}".format(text, str(index))

        extension="jpg"
        image_name = "{}.{}".format(name, extension)
        mask_name = "{}_mask.png".format(name)
        box_name = "{}_boxes.txt".format(name)
        tess_box_name = "{}.box".format(name)


        # Save the image
        output_mask = 0
        output_bboxes = 1
        if out_dir is not None:
            final_image.save(os.path.join(out_dir, image_name))
            if output_mask == 1:
                final_mask.save(os.path.join(out_dir, mask_name))
            if output_bboxes == 1:
                bboxes = [  (object_offset_x, object_offset_y, object_offset_x + resized_img.size[0], object_offset_y + resized_img.size[1]) ]
                save_to_voc_xml(os.path.splitext(image_name)[0], "out", final_image, bboxes)
                with open(os.path.join(out_dir, box_name), "w") as f:
                    for bbox in bboxes:
                        f.write(" ".join([str(v) for v in bbox]) + "\n")
            if output_bboxes == 2:
                bboxes = mask_to_bboxes(final_mask, tess=True)
                with open(os.path.join(out_dir, tess_box_name), "w") as f:
                    for bbox, char in zip(bboxes, text):
                        f.write(" ".join([char] + [str(v) for v in bbox] + ['0']) + "\n")
        else:
            if output_mask == 1:
                return final_image, final_mask
            return final_image




def save_to_voc_xml(image_name, save_folder="out", skiImage=None, bboxes=None, cat_np=None):
    """
    Static Method
    bboxes = None, use internal dataset
    """
    if bboxes is None:
        bboxes = []
        return

    #if cat_np is None:
    #    cat_np = self._cat_index
    if skiImage is None:
        skiImage = self._image_np

    if len(bboxes) == 0:
        return

    width=skiImage.size[0]
    height = skiImage.size[1]
    depth=3
    """
    with Image.fromarray((skiImage).astype(np.uint8)) as img:
        width, height = img.size
        if img.mode == 'YCbCr':
            depth = 3
        else:
            depth = len(img.mode)

        if image_name is None or image_name == "":
            #md5hash = hashlib.md5(img.tobytes())
            #_file_name = md5hash.hexdigest()
            _file_name = "test"
        else:
            _file_name = image_name
            """
    img = skiImage
    _file_name = image_name
    objects = ''
    counter = 0
    database_name = "default"
    image_folder_name = "default"
    image_name = "default"
    for bbox in bboxes:
        # conversion of normalized b-boxes
        if (bbox[0] + bbox[1] + bbox[2] + bbox[3]) < 4:
            bbox[0] = bbox[0] * height
            bbox[1] = bbox[1] * width
            bbox[2] = bbox[2] * height
            bbox[3] = bbox[3] * width

        try:
            _cat_name = bbox[5]
        except:
            _cat_name = "unknown"
            pass

        objects = objects + '''
        	<object>
        		<name>{category_name}</name>
        		<pose>Unspecified</pose>
        		<truncated>0</truncated>
        		<difficult>0</difficult>
        		<bndbox>
        			<xmin>{xmin}</xmin>
        			<ymin>{ymin}</ymin>
        			<xmax>{xmax}</xmax>
        			<ymax>{ymax}</ymax>
        		</bndbox>
        	</object>'''.format(
            category_name=_cat_name,
            xmin=bbox[0],
            ymin=bbox[1],
            xmax=bbox[2],
            ymax=bbox[3]
        )
        counter = counter + 1

    xml = '''<annotation>
        	<folder>{image_folder_name}</folder>
        	<filename>{image_name}</filename>
        	<source>
        		<database>{database_name}</database>
        	</source>
        	<size>
        		<width>{width}</width>
        		<height>{height}</height>
        		<depth>{depth}</depth>
        	</size>
        	<segmented>0</segmented>{objects}
        </annotation>'''.format(
        image_folder_name=image_folder_name,
        image_name=_file_name + ".jpg",
        database_name=database_name,
        width=width,
        height=height,
        depth=depth,
        objects=objects
    )

    try:
        os.mkdir(save_folder)
    except OSError:
        pass

    anno_path = os.path.join(save_folder, _file_name + '.xml')
    with open(anno_path, 'w') as file:
        file.write(xml)
        img.save(save_folder + "/" + _file_name + ".jpg", "JPEG")