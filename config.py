import os

class Configuration(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SECRET_KEY='development key'

DATABASE_CONFIG = {'user':'root', 'password':'@idk'}