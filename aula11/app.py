from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return 'qeeafsadf'

@app.route('/user')
def user():
    products = ['produto 1', 'produto 2']
    return render_template('index.html', products=products)

# tipos de dados recebidos por parametro:
# int, float, string, path
@app.route('/user/<string:username>')
def show_user_profile(username):
    return f'dashboard de {username}!'

@app.route('/user/dashboard/')
def dashboard():
    produtos = ['Feijão']
    return render_template('dashboard.html', produtos=produtos)
if __name__ == '__main__':
    app.run()
