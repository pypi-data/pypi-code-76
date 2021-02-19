import os
from logging_helper import setup_logging
from PIL import ImageFont
logging = setup_logging()

try:
    fonts
except NameError:
    fonts_dir = u'{dir}{sep}'.format(dir=os.path.dirname(os.path.realpath(__file__)),
                                     sep=os.sep)

    base_name, _ = os.path.splitext(os.path.basename(__file__))

    fonts = {}

    for font_file in os.listdir(fonts_dir):
        name, _ = os.path.splitext(font_file)
        if base_name != name:
            fonts[font_file] = os.path.join(fonts_dir, font_file)

if __name__ == u'__main__':
    import pprint
    logging.info(pprint.pformat(fonts))
