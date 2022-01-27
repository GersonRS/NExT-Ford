import enum
import os
from datetime import datetime

from flask import Flask, abort, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/aula15'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app)

db = SQLAlchemy(app)


class StatusChoices(enum.Enum):
    GOOD = 'Good'
    MEDIUM = 'Medium'
    BAD = 'Bad'


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id', ondelete="CASCADE"), nullable=False)
    category = db.relationship(
        'Category', back_populates='products', lazy=True)
    orders = db.relationship("ProductOrder", backref="products")

    def __repr__(self):
        return '<Product %r>' % self.name


class Category(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    products = db.relationship(
        'Product',
        back_populates='category',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        lazy=True,
        passive_deletes=True,
        order_by='desc(Product.name)'
    )

    def __repr__(self):
        return '<Category %r>' % self.name


class Order(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    client_id = db.Column(db.Integer, db.ForeignKey(
        'client.id', ondelete="CASCADE"), nullable=False)
    client = db.relationship(
        'Client', back_populates='order')
    products = db.relationship("ProductOrder", backref="orders")

    def __repr__(self):
        return '<Order %r>' % self.name


class Client(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50))
    telephone_fix = db.Column(db.String(13))
    telephone_celular = db.Column(db.String(14))
    status = db.Column(db.Enum(StatusChoices))
    credit_limit = db.Column(db.Float(2))

    order = db.relationship('Order', back_populates='client', lazy=True)

    def __repr__(self):
        return '<Client %r>' % self.name


class ProductOrder(db.Model, SerializerMixin):
    __tablename__ = 'product_order'
    product_id = db.Column(db.ForeignKey('product.id'), primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id'), primary_key=True)
    amount = db.Column(db.Integer, nullable=False)


@app.before_first_request
def create_db():
    # Delete database file if it exists currently
    if os.path.exists("database.db"):
        os.remove("database.db")
    db.create_all()


class ProductResource(Resource):
    def get(self):
        products = Product.query.all() or abort(404, description="Resource not found")
        return jsonify(
            {"products": [product.to_dict() for product in products]}
        )

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class ProductItemResource(Resource):
    def get(self, product_id):
        product = Product.query.filter_by(id=product_id).first() or abort(
            404, description=f"Resource id {product_id} not found")
        return jsonify(product.to_dict())


class ClientResource(Resource):
    def get(self):
        clients = Client.query.all() or abort(404, description="Resource not found")
        return jsonify(
            {"clients": [client.to_dict() for client in clients]}
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=ascii,
                            help='recurso não enviado, prfv mande um nome')
        args = parser.parse_args()

        client = Client(**args)
        db.session.add(client)
        db.session.commit()

        return jsonify({"success": True, "response": "client added"})

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(ProductResource, "/product/")
api.add_resource(ProductItemResource, "/product/<int:product_id>")

if __name__ == '__main__':
    app.run(debug=True)
