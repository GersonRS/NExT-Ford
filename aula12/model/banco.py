import mysql.connector as connector
# sistema de concessionaria
__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = connector.connect(user='root', password='',
                                         host='localhost', database='aula12')
    return __connection


def create_table():
    cursor = get_connection().cursor()
    query = ('CREATE TABLE IF NOT EXISTS carro(\
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
	marca TEXT NOT NULL, \
	modelo TEXT NOT NULL, \
	ano TEXT, \
	valor DOUBLE(10,2)\
	)')
    cursor.execute(query)


def insert_car(car):
    cursor = get_connection().cursor()
    insert = ('INSERT INTO carro(marca, modelo, ano, valor) VALUES(%s, %s, %s, %s)')
    data = (car['marca'], car['modelo'], car['ano'], car['valor'])
    cursor.execute(insert, data)
    get_connection().commit()
    return cursor.lastrowid


def update_car(car):
    cursor = get_connection().cursor()
    query = (
        'UPDATE carro SET marca = %s, modelo = %s, ano = %s, valor = %s WHERE id = %s')
    data = (car['marca'], car['modelo'], car['ano'], car['valor'], car['id'])
    cursor.execute(query, data)
    get_connection().commit()
    return cursor.lastrowid


def delete_car(car):
    cursor = get_connection().cursor()
    query = ('DELETE FROM carro WHERE id = %s')
    data = (car['id'], )
    cursor.execute(query, data)
    get_connection().commit()
    return cursor.lastrowid


def search_car(id):
    cursor = get_connection().cursor()
    query = ('SELECT * FROM carro WHERE id = %s')
    data = (id, )
    cursor.execute(query, data)
    return cursor.fetchone()


def lista_carros():
    cursor = get_connection().cursor()
    query = ('select * from carro')
    cursor.execute(query)
    # return cursor.fetchmany(size=2)
    return cursor.fetchall()


def desconnect():
    get_connection().close()
    __connection = None
