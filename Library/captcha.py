import random
import string
from glob import glob
from os import path

from PIL import Image, ImageDraw, ImageFont

DATA_DIR = path.abspath(path.dirname(__file__))


class ImgCaptcha:
    def __init__(self, c_height=200, c_width=600, red=None,
                 green=None, blue=None,
                 font_type=None, font_color="WHITE", font_size=50):
        self.Height = c_height
        self.Width = c_width
        self.rgb_colors = self.color_gen(red, green, blue)
        self.font_type = font_type
        self.font_color = font_color
        self.font_size = font_size
        self.select_font()
        self._Image = None
        self._Image_New = None
        self.Draw = None
        self.Image_Buf = None

    def select_font(self):
        if self.font_type is not None:
            return self.font_type
        fonts = glob(path.join(DATA_DIR, "Fonts", "*.ttf"))
        self.font_type = fonts[random.randint(0, len(fonts) - 1)]

    @staticmethod
    def color_gen(red, green, blue):
        red = random.randint(50, 255) if red is None else red
        green = random.randint(50, 255) if green is None else green
        blue = random.randint(50, 255) if blue is None else blue
        return red, green, blue

    def gen_image(self, captcha_string=None, captcha_length=6):
        if captcha_string is None:
            captcha_string = gen_random(captcha_length)
        self._Image = Image.new(mode='RGBA', size=(self.Width, self.Height),
                                color=self.rgb_colors)
        letter_width = (self.Width // len(captcha_string))
        self.draw_letters(captcha_string=captcha_string, width=letter_width)
        self.__add_noise()

    def show_image(self):
        self._Image.show()

    def save_image(self, filename="Captcha.png", file_format="PNG"):
        """
        Save the Image to given path
        :param filename: /file/path/filename
        :param file_format: format extension of image
        :return:
        """
        self._Image.save(filename, format=file_format)

    def draw_letters(self, captcha_string, width):
        """
        :param width: width for one letter
        :param captcha_string: Text to print
        :return: Image
        """
        x_offset = 0
        sample_img = Image.new(mode='RGBA', size=(width, self.Height))

        for letter in captcha_string:
            new_text_img = Image.new(mode='RGBA', size=(width, self.Height),
                                     color=self.rgb_colors)
            text_img = ImageDraw.Draw(new_text_img)

            width_text, height_text = text_img.textsize(letter,
                                                        font=ImageFont.truetype(
                                                            self.font_type,
                                                            self.font_size))
            text_left = (width - width_text) / 5
            text_top = (self.Height - height_text) / 3
            text_img.text(xy=(text_left, text_top), text=letter,
                          font=ImageFont.truetype(self.font_type,
                                                  self.font_size),
                          fill=self.font_color)
            transparent_text = Image.alpha_composite(sample_img, new_text_img)

            rotation = random.randint(-40, 40)
            rotated_img = transparent_text.rotate(rotation, expand=0)
            self._Image.paste(rotated_img, (x_offset, 0), mask=rotated_img)
            x_offset += new_text_img.size[0]

    def __add_noise(self, density=1000):
        def rand_int(start, end):
            return random.randint(start, end)

        line_x1 = rand_int(0, self.Width * .3)
        line_x2 = rand_int(self.Width * 0.60, self.Width)
        line_y1 = rand_int(self.Height * 0.25, self.Height * 0.75)
        line_y2 = rand_int(self.Height * 0.25, self.Height * 0.75)
        distort_image = ImageDraw.Draw(self._Image)
        self.draw_line(distort_image, (line_x1, line_y1, line_x2, line_y2))
        while density:
            x = rand_int(0, self.Width)
            y = rand_int(0, self.Height)
            self.draw_point(distort_image, cords=(x, y))
            density -= 1

    @staticmethod
    def draw_point(obj, cords=(64, 16, 66, 18)):
        obj.point(cords)

    def draw_line(self, obj, cords, line_width=4):
        obj.line(cords, width=line_width, fill=self.font_color)


def gen_random(length=6, constants=None):
    """
    :param constants: The mixture of characters for captcha
    :param length: Length of Captcha
    :return: Captcha String
    """
    if constants is None:
        constants = ["U", "L", "D"]
    string_constants = {
        "U": string.ascii_uppercase,
        "L": string.ascii_lowercase,
        "D": string.digits,
        "P": string.punctuation
    }
    all_string = ""
    for case in constants:
        all_string += string_constants[case]
    captcha_string = ''.join(random.choices(all_string, k=length))
    return captcha_string


if __name__ == "__main__":
    image = ImgCaptcha()
    image.gen_image()
    image.show_image()
    image.save_image("Captcha1.png")
