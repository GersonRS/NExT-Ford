
from model.modelos import Carro
from model.banco import insert_car, lista_carros, search_car, update_car

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'flask'
def formatar(car):
    text = str(car.valor)[:3]+"."+str(car.valor)[3:].replace('.',',')
    car.valor = f'R$ {text}'
    return car

@app.route('/')
def index():
    carros = lista_carros()
    carros = map(formatar, carros)
    return render_template('index.html', title='Lista de Carros', carros=carros)


@app.route('/novo')
def novo():
    return render_template('newcar.html', title='Novo Carro')

@app.route('/atualizar/<id>')
def atualizar(id):
    carro = search_car(id)
    return render_template('updatecar.html', title='Atualizar Carro', carro=carro)


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

@app.route('/update', methods=['POST', ])
def update():
    id = request.form['id']
    marca = request.form['marca']
    modelo = request.form['modelo']
    ano = request.form['ano']
    valor = request.form['valor']
    try:
        update_car(Carro(id, marca, modelo, ano, valor))
        flash('Carro alterado com sucesso!')
    except:
        flash('Não foi possivel alterar o carro!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
