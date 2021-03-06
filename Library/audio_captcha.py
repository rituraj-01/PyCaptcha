from gtts import gTTS
from gen_captcha import CaptchaGenerator


class TextToSpeech(object):
    def __init__(self, string_length=6, string_constants=("L", "D")):
        self.generator_obj = CaptchaGenerator(string_length, string_constants)

    def gen_audio(self, filename="aud.mp3", captcha_string=None):
        if captcha_string is None:
            captcha_string = self.generator_obj.gen_random_str()
        tts = gTTS(captcha_string, lang='en', slow=True)
        tts.save(filename)


if __name__ == "__main__":
    text_to_speech = TextToSpeech()
    text_to_speech.gen_audio()

