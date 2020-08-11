ouclass Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    # Normal Configurtion
    SECRET_KEY = "Make_Your_Own_Key"
    UPLOAD_FOLDER = r'Uploaded Documnet//'

    # Mail Server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'Your_Gmail@gmail.com'
    MAIL_PASSWORD = 'Password_of_Your_Gmail'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Database configuration
    MYSQL_HOST = 'Localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'YourDB'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "Make_Your_Own_Key"
    UPLOAD_FOLDER = r'Uploaded Documnet//'

    # Mail Server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'Your_Gmail@gmail.com'
    MAIL_PASSWORD = 'Password_of_Your_Gmail'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Database configuration
    MYSQL_HOST = 'Localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'YourDB'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "Make_Your_Own_Key"
    UPLOAD_FOLDER = r'Uploaded Documnet//'

    # Mail Server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'Your_Gmail@gmail.com'
    MAIL_PASSWORD = 'Password_of_Your_Gmail'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Database configuration
    MYSQL_HOST = 'Localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'YourDB'
