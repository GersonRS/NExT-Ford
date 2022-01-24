from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/aula13'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.txt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


@app.before_first_request
def create_db():
    db.create_all()


@app.route('/cars', methods=['GET'])
def list_cars():
    cars = Car.query.all() or abort(404)
    return jsonify(
        {"cars": [car.to_dict() for car in cars]}
    )


@app.route('/cars', methods=['POST'])
def create_car():
    data = request.json

    brand = data['brand']
    model = data['model']
    year = data['year']
    value = data['value']

    car = Car(brand=brand, model=model, year=year, value=value)
    db.session.add(car)
    db.session.commit()

    return jsonify({"success": True, "response": "Car added"})


@app.route('/cars/<car_id>', methods=['GET'])
def retrive_car(car_id):
    car = Car.query.filter_by(id=car_id).first() or abort(404)
    return jsonify(car.to_dict())


@app.route('/cars/<car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.filter_by(id=car_id).first() or abort(404)

    data = request.get_json()

    if data.get('brand'):
        car.brand = data.get('brand')
    if data.get('model'):
        car.model = data.get('model')
    if data.get('year'):
        car.year = data.get('year')
    if data.get('value'):
        car.value = data.get('value')

    db.session.add(car)
    db.session.commit()

    return jsonify(car.to_dict())


@app.route('/cars/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.filter_by(id=car_id).first() or abort(404)
    db.session.delete(car)
    db.session.commit()
    return jsonify(car.to_dict())


class Car(db.Model, SerializerMixin):
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100))
    value = db.Column(db.Float(2))

    def __init__(self, brand, model, year, value):
        self.brand = brand
        self.model = model
        self.year = year
        self.value = value

    def __repr__(self):
        return f'{self.brand} brand car, {self.model} model!'


if __name__ == '__main__':
    app.run()
