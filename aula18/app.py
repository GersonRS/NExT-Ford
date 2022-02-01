from flask import Flask

from aula18.ext import database
from aula18.ext import config
from aula18.ext import site
from aula18.ext import api
from aula18.ext import cli


app = Flask(__name__)
config.init_app(app)
database.init_app(app)
cli.init_app(app)
site.init_app(app)
api.init_app(app)
