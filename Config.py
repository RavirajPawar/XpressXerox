class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    # Normal Configurtion
    SECRET_KEY = "raviraj+Amir+both+developed"
    UPLOAD_FOLDER = r'Uploaded Documnet//'

    # Mail Server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'xpressxeroxx@gmail.com'
    MAIL_PASSWORD = 'AmirAdmin'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Database configuration
    MYSQL_HOST = 'xpressxerox.mysql.pythonanywhere-services.com'
    MYSQL_USER = 'xpressxerox'
    MYSQL_PASSWORD = 'rootroot'
    MYSQL_DB = 'xpressxerox$Amir'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "raviraj+Amir+both+developed"
    UPLOAD_FOLDER = r'Uploaded Documnet//'

    # Mail Server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'xpressxeroxx@gmail.com'
    MAIL_PASSWORD = 'AmirAdmin'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Database configuration
    MYSQL_HOST = 'xpressxerox.mysql.pythonanywhere-services.com'
    MYSQL_USER = 'xpressxerox'
    MYSQL_PASSWORD = 'rootroot'
    MYSQL_DB = 'xpressxerox$Amir'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "raviraj+Amir+both+developed"
    UPLOAD_FOLDER = r'Uploaded Documnet//'

    # Mail Server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'xpressxeroxx@gmail.com'
    MAIL_PASSWORD = 'AmirAdmin'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Database configuration
    MYSQL_HOST = 'xpressxerox.mysql.pythonanywhere-services.com'
    MYSQL_USER = 'xpressxerox'
    MYSQL_PASSWORD = 'rootroot'
    MYSQL_DB = 'xpressxerox$Amir'