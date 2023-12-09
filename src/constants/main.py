import os.path

ROOT_DIR = ''


class Logging:
    CONFIG_FILE_PATH = os.path.join(ROOT_DIR, 'src', 'configs', 'logging_config.ini')


class Google:
    OAUTH_CLIENT_SECRET = os.path.join(ROOT_DIR, 'src', 'configs',
                                       '')
    TOKEN = os.path.join(ROOT_DIR, 'src', 'configs', 'token.json')


class Presentation:
    SLIDE_ID_PREFIX = 'slide'
    ELEMENT_ID_PREFIX = 'element'


# Following dimensions are in PT
# Slide width = 10 inches = 720 PT
# Slide height = 5.625 inches = 405 PT
class Properties:
    TITLE_PROPERTIES = {
        'height_magnitude': 50,
        'width_magnitude': 680,
        'translateX': 20,
        'translateY': 20,
        'text': 'HEADING'
    }
    BODY_PROPERTIES = {
        'height_magnitude': 305,
        'width_magnitude': 680,
        'translateX': 20,
        'translateY': 80
    }
