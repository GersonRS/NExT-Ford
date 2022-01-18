import mysql.connector as connector
# sistema de concessionaria


def connection():
    cnx = connector.connect(user='root', password='',
                            host='localhost', database='aula9')
    return cnx


def create_table(cnx):
    cursor = cnx.cursor()
    query = ('CREATE TABLE IF NOT EXISTS carro(\
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
    marca TEXT NOT NULL, \
    modelo TEXT NOT NULL, \
    ano TEXT, \
    valor DECIMAL(10,2)\
    )')
    cursor.execute(query)


def insert_car(cnx, car):
    cursor = cnx.cursor()
    insert = ('INSERT INTO carro(marca, modelo, ano, valor) VALUES(%s, %s, %s, %s)')
    data = (car['marca'], car['modelo'], car['ano'], car['valor'])
    cursor.execute(insert, data)
    cnx.commit()


def update_car(cnx, car):
    pass


def delete_car(cnx, car):
    pass


def search_car(cnx, modelo):
    cursor = cnx.cursor()
    insert = (f"SELECT * FROM carro WHERE modelo like '{modelo}%'")
    cursor.execute(insert)
    return cursor.fetchone()

def lista_carros(cnx):
    cursor = cnx.cursor()
    query = ('select * from carro')
    cursor.execute(query)
    return cursor.fetchmany(size=2)
    # return cursor.fetchall()


def desconnect(cnx):
    cnx.close()

# if __name__ == '__main__':
    # connector = connection()
    # # create_table(connector)
    # print('1 - Cadastrar carro')
    # print('2 - Atualizar carro')
    # print('3 - Buscar carro')
    # print('4 - Deletar carro')
    # print('5 - Listar todos os carros')
    # option = int(input('Escolha um numero da opção: '))

    # if option == 1:
    #     marca = input('Digite a marca do carro: ')
    #     modelo = input('Digite a modelo do carro: ')
    #     ano = input('Digite a ano do carro: ')
    #     valor = input('Digite a valor do carro: ')
    #     insert_car(connector, {
    #         'marca': marca,
    #         'modelo': modelo,
    #         'ano': ano,
    #         'valor': valor
    #     })
    # elif option == 2:
    #     marca = input('Digite o modelo do carro que quer alterar: ')
    # elif option == 3:
    #     modelo = input('Digite o modelo do carro que quer exibir: ')
    #     print(search_car(connector, modelo))
    # elif option == 4:
    #     carro = input('Digite o modelo do carro que quer deletar: ')
    # elif option == 5:
    #     print(lista_carros(connector))
    # else:
    #     print('Digite uma opção valida, na proxima vez!')
    # desconnect(connector)


from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'Servidor ativo'
app.run()
