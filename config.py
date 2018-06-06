#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" config.py: Configurações gerais compartilhadas """

from os import path

DATABASE_CONFIG = {'user':'root', 'password':'@idk'} # Usuário e senha do MariaDB

class Configuration(object):
    """ Configurações do Flask e do Jinja2 """
    APPLICATION_DIR = path.dirname(path.realpath(__file__))
    DEBUG = True
    SECRET_KEY='development key'
