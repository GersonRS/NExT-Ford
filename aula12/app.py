
from model.modelos import Carro
from model.banco import insert_car, lista_carros

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'flask'


@app.route('/')
def index():
    carros = lista_carros()
    return render_template('index.html', title='Lista de Carros', carros=carros)


@app.route('/novo')
def novo():
    return render_template('newcar.html', title='Novo Carro')


@app.route('/criar', methods=['POST', ])
def criar():
    marca = request.form['marca']
    modelo = request.form['modelo']
    ano = request.form['ano']
    valor = request.form['valor']
    try:
        insert_car(Carro(0, marca, modelo, ano, valor))
        flash('Carro criado com sucesso!')
    except:
        flash('Não foi possivel cadastrar o carro!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
