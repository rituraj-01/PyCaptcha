import string
from random import choices


class CaptchaGenerator:
    def __init__(self, string_length, constants=("U", "L", "D")):
        """
        :param constants: The mixture of characters for captcha
        """
        self.string_length = string_length
        self.constants = constants
        self.string_constants = {
            "U": string.ascii_uppercase,
            "L": string.ascii_lowercase,
            "D": string.digits,
            "P": string.punctuation
        }
        self.all_string = ""
        for case in self.constants:
            self.all_string += self.string_constants[case]

    def gen_random_str(self, length=6):
        """
        :param length: Length of Captcha
        :return: Captcha String
        """
        captcha_string = ''.join(choices(self.all_string,
                                                k=self.string_length))
        return captcha_string

