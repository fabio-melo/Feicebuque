#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" App.py - Instanciador do Aplicativo e Configurações """

from flask import Flask
from os import path
from config import Configuration

""" Inicializar o Flask, e carregar as configurações """

app = Flask(__name__)
app.config.from_object(Configuration) 

