import os
import sys


class Project:
    def __init__(self, proj):
        self.proj = proj

        self.requirements = "flask\nflask-sqlalchemy\nflask-migrate\nflask-admin\ndynaconf\nmysql-connector-python\nFlask-RESTful\nSQLAlchemy-serializer"
        self.requirements_dev = (
            "black\nflake8\nflask-debugtoolbar\nflask-shell-ipython\nipdb\n"
            "ipython\nisort\npytest\npytest-flask\npytest-cov\n"
        )
        self.makefile = (
            "clean:\n"
            "\t@find ./ -name '*.pyc' -exec rm -f {} \;\n"
            "\t@find ./ -name 'Thumbs.db' -exec rm -f {} \;\n"
            "\t@find ./ -name '*~' -exec rm -f {} \;\n"
            "\trm -rf .cache\n"
            "\trm -rf build\n"
            "\trm -rf dist\n"
            "\trm -rf *.egg-info\n"
            "\trm -rf htmlcov\n"
            "\trm -rf .tox/\n"
            "\trm -rf docs/_build\n\n"
            "install:\n"
            "\tpip install -e .\n\n"
            "install-dev:\n"
            "\tpip install -e .['dev']\n\n"
            "test:\n"
            f"\tpytest tests/ -v --cov={self.proj}\n\n"
            "run:\n"
            f"\tFLASK_APP={self.proj}/app.py flask run\n\n"
            "run-dev:\n"
            f"\tFLASK_APP={self.proj}/app.py FLASK_ENV=development flask run\n\n"
            f"init_db:\n"
            f"	FLASK_APP={self.proj}/app.py flask create-db\n"
            f"	FLASK_APP={self.proj}/app.py flask db upgrade\n\n"
            "test:\n"
            f"	FLASK_ENV=test pytest tests/ -v --cov={self.proj}\n\n"
            "format:\n"
            "	isort **/*.py\n"
            "	black -l 79 **/*.py\n\n"
            "run:\n"
            f"	FLASK_APP={self.proj}/app.py FLASK_ENV=development flask run\n"
        )
        self.setup = (
            "from setuptools import setup, find_packages\n\n"
            "def read(filename):\n"
            "    return [rq.strip() for rq in open(filename).readlines()]\n\n"
            "setup(\n"
            f"    name='{self.proj}',\n"
            "    version='0.1.0',\n"
            f"    description='{self.proj} project',\n"
            "    packages=find_packages(),\n"
            "    include_package_data=True,\n"
            "    install_requires=read('requirements.txt'),\n"
            "    extras_require={\n"
            "        'dev': read('requirements-dev.txt')\n"
            "    }\n"
            ")\n"
        )
        self.conftest = (
            "import pytest\n\n"
            f"from {self.proj}.app import create_app\n\n"
            "@pytest.fixture(scope='module')\n"
            "def app():\n"
            "    '''Instance of main flask app'''\n"
            "    return create_app()\n"
        )
        self.test_app = (
            "def test_app_is_created(app):\n"
            f"    assert app.name == '{self.proj}.app'\n\n"
            "def test_config_is_loaded(config):\n"
            "    assert config['DEBUG'] is False"
            " # is True if FLASK_ENV=development\n\n"
            "def test_request_returns_404(client):\n"
            "    assert client.get('/some_invalid_route').status_code == 404\n"
        )
        self.main_py_site = (
            "from flask import Blueprint\n\n"
            "bp = Blueprint('site', __name__)\n\n"
            "@bp.route('/')\n"
            "def index():\n"
            f"    return 'Hello, {self.proj.upper()}!'\n"
        )
        self.init_py_site = (
            "from .main import bp\n\n"
            "def init_app(app):\n"
            "    app.register_blueprint(bp)\n"
        )
        self.init_py_db = (
            "from flask_migrate import Migrate\n"
            "from flask_sqlalchemy import SQLAlchemy\n\n"
            "migrate = Migrate()\n"
            "db = SQLAlchemy()\n\n"
            "def init_app(app):\n"
            "    db.init_app(app)\n"
            "    migrate.init_app(app, db)\n"
        )
        self.init_py_config = (
            "from dynaconf import FlaskDynaconf\n\n"
            "def init_app(app):\n"
            "   FlaskDynaconf(app)\n"
            "   app.config.load_extensions('EXTENSIONS')\n"
        )
        self.settings = (
            f'''[default]
DEBUG = false
FLASK_ADMIN_SWATCH = "cerulean"
APP_NAME = "{self.proj}"
EXTENSIONS = [
	"{self.proj}.ext.db:init_app",
	"{self.proj}.ext.auth:init_app",
	"{self.proj}.ext.admin:init_app",
	"{self.proj}.ext.cli:init_app",
	"{self.proj}.ext.site:init_app",
]

[development]
DEBUG = true
SQLALCHEMY_DATABASE_URI = "sqlite:///{self.proj}.db"
SQLALCHEMY_TRACK_MODIFICATIONS = false
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = true
DEBUG_TB_PROFILER_ENABLED = true
DEBUG_TB_INTERCEPT_REDIRECTS = false
APP_NAME = "{self.proj} (dev mode)"
EXTENSIONS = [
	"{self.proj}.ext.db:init_app",
	"{self.proj}.ext.auth:init_app",
	"{self.proj}.ext.admin:init_app",
	"{self.proj}.ext.cli:init_app",
	"{self.proj}.ext.toolbar:init_app",
	"{self.proj}.ext.site:init_app",
]


[production]
SQLALCHEMY_TRACK_MODIFICATIONS = false
SQLALCHEMY_DATABASE_URI = "mysql://...."'''
        )

        self.app = (
            "from flask import Flask\n"
            f"from {self.proj}.ext import config\n\n\n"
            "def create_app():\n"
            "	'''Factory to create a Flask app based on factory pattern'''\n"
            "	app = Flask(__name__)\n"
            f"	config.init_app(app)\n"
            "	return app\n"
        )

        self.admin = (
            '''from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from delivery.ext.db import db

admin = Admin()


def init_app(app):
    admin.name = app.config.get("APP_NAME", "CodeFoods")
    admin.template_mode = app.config.get("APP_TEMPLATE_MODE", "bootstrap2")
    admin.init_app(app)

    # TODO: Proteger com senha
    # TODO: traduzir para PTBR

    #admin.add_view(ModelView(Category, db.session))'''
        )

        self.commands = (
            f'''from {self.proj}.ext.db import db


def create_db():
	"""Creates database"""
	db.create_all()


def drop_db():
	"""Cleans database"""
	db.drop_all()
'''
        )

        self.base_html = (
            '''<!DOCTYPE html>
<html>
<head>
	{% block head %}
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Hello Bulma!</title>
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
	{% endblock head %}
	{%block  extra_css %} {% endblock extra_css %}
</head>
<body>
{% block nav %}
<nav class="navbar" role="navigation" aria-label="main navigation">
	<div class="navbar-brand">
	<a class="navbar-item" href="https://bulma.io">
		<strong>CodeFoods</strong>
	</a>

	<a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
		<span aria-hidden="true"></span>
		<span aria-hidden="true"></span>
		<span aria-hidden="true"></span>
	</a>
	</div>

	<div id="navbarBasicExample" class="navbar-menu">
	<div class="navbar-start">
		<a class="navbar-item" href="/">
		Home
		</a>

		<div class="navbar-item has-dropdown is-hoverable">
		<a class="navbar-link">
			level
		</a>

		<div class="navbar-dropdown">
			<a class="navbar-item">
			item 1
			</a>
			<a class="navbar-item">
			item 2
			</a>
			<hr class="navbar-divider">
			<a class="navbar-item">
			item 3
			</a>
		</div>
		</div>
	</div>

	<div class="navbar-end">
		<div class="navbar-item">
		<div class="buttons">
			<a class="button is-primary">
			<strong>Sign up</strong>
			</a>
			<a class="button is-light">
			Log in
			</a>
		</div>
		</div>
	</div>
	</div>
</nav>
{% endblock nav%}
{% block top%}{% endblock top %}
<section class="section">
	<div class="container">
		{% block main %}{% endblock main%}
	</div>
</section>
{% block footer %}
<footer class="footer">
	<div class="content has-text-centered">
	<p>
		<strong>Bulma</strong> by <a href="https://jgthms.com">Jeremy Thomas</a>. The source code is licensed
		<a href="http://opensource.org/licenses/mit-license.php">MIT</a>. The website content
		is licensed <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY NC SA 4.0</a>.
	</p>
	</div>
</footer>
{% endblock footer%}
</body>
</html>'''
        )

    def dir_extrutures(self):
        print("\n1 - Creating the directories extruture ...")
        # /
        os.system(f"mkdir {self.proj}")
        # /proj
        os.system(f"mkdir {self.proj}/{self.proj}")
        # /proj/templates
        os.system(f"mkdir {self.proj}/{self.proj}/templates")
        # /proj/static (css, img, js)
        os.system(f"mkdir {self.proj}/{self.proj}/static")
        os.system(f"mkdir {self.proj}/{self.proj}/static/css")
        os.system(f"mkdir {self.proj}/{self.proj}/static/img")
        os.system(f"mkdir {self.proj}/{self.proj}/static/js")
        # /proj/ext
        os.system(f"mkdir {self.proj}/{self.proj}/ext")
        # /proj/ext/site
        os.system(f"mkdir {self.proj}/{self.proj}/ext/site")

        os.system(f"mkdir {self.proj}/{self.proj}/ext/db")
        os.system(f"mkdir {self.proj}/{self.proj}/ext/api")
        os.system(f"mkdir {self.proj}/{self.proj}/ext/auth")
        # /proj/tests
        os.system(f"mkdir {self.proj}/tests")

    def write_files(self):
        print("2 - Writing texts content in files ...")
        # /
        os.system(f"touch {self.proj}/LICENCE")
        os.system(f"touch {self.proj}/README.md")
        with open(f"{self.proj}/requirements.txt", "w") as fl:
            fl.write(self.requirements)
        with open(f"{self.proj}/requirements-dev.txt", "w") as fl:
            fl.write(self.requirements_dev)
        with open(f"{self.proj}/Makefile", "w") as fl:
            fl.write(self.makefile)
        with open(f"{self.proj}/setup.py", "w") as fl:
            fl.write(self.setup)
        # /proj
        os.system(f"touch {self.proj}/{self.proj}/__init__.py")
        with open(f"{self.proj}/{self.proj}/app.py", "w") as fl:
            fl.write(self.app)
        # /test
        with open(f"{self.proj}/tests/conftest.py", "w") as fl:
            fl.write(self.conftest)
        with open(f"{self.proj}/tests/test_app.py", "w") as fl:
            fl.write(self.test_app)
        # /proj/ext
        os.system(f"touch {self.proj}/{self.proj}/ext/__init__.py")

        # /proj/ext/site
        with open(f"{self.proj}/{self.proj}/ext/site/main.py", "w") as fl:
            fl.write(self.main_py_site)
        with open(f"{self.proj}/{self.proj}/ext/site/__init__.py", "w") as fl:
            fl.write(self.init_py_site)

        # /proj/ext/config
        with open(f"{self.proj}/{self.proj}/ext/config.py", "w") as fl:
            fl.write(self.init_py_config)
		# /proj/ext/admin
        with open(f"{self.proj}/{self.proj}/ext/admin.py", "w") as fl:
            fl.write(self.admin)
        # /proj/ext/db
        with open(f"{self.proj}/{self.proj}/ext/db/__init__.py", "w") as fl:
            fl.write(self.init_py_db)
        with open(f"{self.proj}/{self.proj}/ext/db/commands.py", "w") as fl:
            fl.write(self.commands)
        with open(f"{self.proj}/{self.proj}/ext/toolbar.py", "w") as fl:
            fl.write('''from flask_debugtoolbar import DebugToolbarExtension


def init_app(app):
	if app.debug:
		DebugToolbarExtension(app)
            ''')
        with open(f"{self.proj}/{self.proj}/ext/cli.py", "w") as fl:
            fl.write(f'''import click

from {self.proj}.ext.db.commands import create_db, drop_db


def init_app(app):

	app.cli.add_command(app.cli.command()(create_db))
	app.cli.add_command(app.cli.command()(drop_db))

	@app.cli.command()
	def listar_coisas():
		# TODO: usar tabulate e listar coisas
		click.echo("lista de coisas")''')
        with open(f"{self.proj}/{self.proj}/ext/db/models.py", "w") as fl:
            pass
        with open(f"{self.proj}/{self.proj}/templates/base.html", "w") as fl:
            fl.write(self.base_html)
        with open(f"{self.proj}/settings.toml", "w") as fl:
            fl.write(self.settings)
        with open(f"{self.proj}/secrets.toml", "w") as fl:
            fl.write(f"""[default]
SECRET_KEY = {str(os.urandom(16))[1:]}""")

    def create_venv(self):
        print("3 - Creating virtual env (.venv) ...")
        os.chdir(f"{self.proj}")
        os.system("python3 -m venv .venv")
        os.system(".venv/bin/pip install -q --upgrade pip")
        os.system(".venv/bin/pip install -q -r requirements.txt")


# Starting project #############################################################

print("\n### Flask Project Builder ###\n")

proj, venv = "", None

# trying to get: proj and venv on the command line
if sys.argv[1:]:
    proj = sys.argv[1]
    venv = True if "--venv" in sys.argv[1:] else False

while not proj:
    print("Enter the project name.")
    proj = input().replace(" ", "_")

# to use a virtual environment?
# if not venv:
#     print("Do you want to use the .venv? (Y/n)")
#     venv = True if input() in "YySs" else False

project = Project(proj)
project.dir_extrutures()
project.write_files()
if venv:
    project.create_venv()

print("\nAll done!")
