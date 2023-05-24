from dotenv import load_dotenv
import os
from os import urandom
from datetime import timedelta

load_dotenv("./config/.env")

class Config:
    ENV = 'default'
    DEBUG = False
    TESTING = False

    # Secret Key Config.
    SECRET_KEY = urandom(24)

    # SQL Alchemy Config.
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # Cross-Origin Resource Sharing Config.
    CORS_ALLOWED_ORIGINS = '*'

    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    ENV = os.getenv('MODE')
    DEBUG = True
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['LINE_CHANNEL_ACCESS_TOKEN'] = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        app.config['LINE_CHANNEL_SECRET'] = os.getenv('LINE_CHANNEL_SECRET')
        
        # Model Initialize.
        from utility.sql_alchemy import initialize
        initialize(app)

        # line bot Initialize
        from utility.line_bot import initialize
        initialize(app)



class ReleaseConfig(Config):
    ENV = os.getenv('MODE')
    DEBUG = True
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['LINE_CHANNEL_ACCESS_TOKEN'] = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        app.config['LINE_CHANNEL_SECRET'] = os.getenv('LINE_CHANNEL_SECRET')

        
        # Model Initialize.
        from utility.sql_alchemy import initialize
        initialize(app)

        # line bot Initialize
        from utility.line_bot import initialize
        initialize(app)




config = {
    'local': LocalConfig,
    'release' : ReleaseConfig
}
