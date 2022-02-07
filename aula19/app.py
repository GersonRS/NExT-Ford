from flask import Flask

from aula19.ext import database
from aula19.ext import config
from aula19.ext import site
from aula19.ext import api
from aula19.ext import cli
from aula19.ext import auth


app = Flask(__name__)
config.init_app(app)
database.init_app(app)
cli.init_app(app)
site.init_app(app)
api.init_app(app)
auth.init_app(app)


@app.before_first_request
def init_db():
    database.db.create_all()