from googletrans import Translator

translator = Translator()

def translate_text(text,target):
    return translator.translate(
        text,
        dest=target
    ).text