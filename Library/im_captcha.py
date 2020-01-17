import random
from os import path
from gen_captcha import CaptchaGenerator
from PIL import Image, ImageDraw, ImageFont

DATA_DIR = path.abspath(path.dirname(__file__))


class CaptchaImager:
    def __init__(self):
        self.font_type = None
        self.font_size = None
        self.font_color = None
        self.Width = None
        self.Height = None
        self._Image = None
        self.rgb_colors = None

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

    def add_noise(self, density=1000):
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


class ImageCaptcha(CaptchaImager):
    def __init__(self, c_height=80, c_width=240, c_color="#B89843",
                 font_type=None, font_color="WHITE", font_size=50,
                 string_length=6, string_constants=("U", "L", "D")):
        super().__init__()
        self.generator_obj = CaptchaGenerator(string_length, string_constants)
        self.Height = c_height
        self.Width = c_width
        self.rgb_colors = c_color
        self.font_type = self.select_font(font_type)
        self.font_color = font_color
        self.font_size = font_size
        self._Image = None
        self._Image_New = None
        self.Draw = None
        self.Image_Buf = None

    @staticmethod
    def select_font(font):
        if font is None:
            return path.join(DATA_DIR, "Fonts", "InriaSerif-Regular.ttf")
        else:
            return font

    def generate(self, captcha_string=None, noise_density=1000):
        if captcha_string is None:
            captcha_string = self.generator_obj.gen_random_str()
        self._Image = Image.new(mode='RGBA', size=(self.Width, self.Height),
                                color=self.rgb_colors)
        letter_width = (self.Width // len(captcha_string))
        super().draw_letters(captcha_string=captcha_string,
                             width=letter_width)
        super().add_noise(density=noise_density)
        return captcha_string

    def save_image(self, filename="Captcha.png", file_format="PNG"):
        self._Image.save(filename, format=file_format)

    def im_bytes(self, encoder="raw"):
        return self._Image.tobytes(encoder_name=encoder)

    def show_image(self):
        self._Image.show()


if __name__ == "__main__":
    image = ImageCaptcha()
    image.generate()
    image.save_image()
    image.show_image()
