
# from .controller import main as application_root
import time
import os
from flask import Flask
from utility.sql_alchemy.globals import sqlAlchemy_manager
# from model import *





def create_db():
    sqlAlchemy_manager.create_all()

def create_app(mode: str):

    app = Flask(__name__)

    from config import config
    app.config.from_object(config[mode])
    config[mode].init_app(app)

    from .controller import main
    app.register_blueprint(main)

    from .line import line
    app.register_blueprint(line)


    return app
