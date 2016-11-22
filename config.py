import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'insert_secret_key_here'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    REDDIT_USER_AGENT = os.environ.get('REDDIT_USER_AGENT') or \
        'insert a proper reddit user agent here'
    REDDIT_APP_ID = os.environ.get('REDDIT_APP_ID') or \
        'insert_reddit_app_id_here'
    REDDIT_APP_SECRET = os.environ.get('REDDIT_APP_SECRET') or \
        'insert_reddit_app_secret'
    OAUTH_REDIRECT_URI = os.environ.get('OAUTH_REDIRECT_URI') or \
        'http://localhost:5000/authorize'
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or \
        'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or \
        'admin'
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID') or \
        'U-XXXX-YY'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data_dev.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
