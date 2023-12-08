import os.path

ROOT_DIR = ''


class Logging:
    CONFIG_FILE_PATH = os.path.join(ROOT_DIR, 'src', 'configs', 'logging_config.ini')


class Google:
    OAUTH_CLIENT_SECRET = os.path.join(ROOT_DIR, 'src', 'configs',
                                       '')
    TOKEN = os.path.join(ROOT_DIR, 'src', 'configs', 'token.json')
