
class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    try:
        from local_config import SECRET_KEY, \
            SQLALCHEMY_DATABASE_URI
    except ImportError:
        pass