import enum
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from aula19.ext.database import db


class StatusChoices(enum.Enum):
    GOOD = 'Good'
    MEDIUM = 'Medium'
    BAD = 'Bad'


class Product(db.Model, SerializerMixin):

    serialize_rules = ('-category.products', '-orders', 'qtd')

    def qtd(self):
        return len(self.orders)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id', ondelete="CASCADE"), nullable=False)
    category = db.relationship(
        'Category', back_populates='products', lazy=True)
    orders = db.relationship("ProductOrder", backref="products")


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


class Client(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50))
    telephone_fix = db.Column(db.String(13))
    telephone_celular = db.Column(db.String(14))
    status = db.Column(db.Enum(StatusChoices))
    credit_limit = db.Column(db.Float(2))

    order = db.relationship('Order', back_populates='client', lazy=True)


class ProductOrder(db.Model, SerializerMixin):
    __tablename__ = 'product_order'
    product_id = db.Column(db.ForeignKey('product.id'), primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id'), primary_key=True)
    amount = db.Column(db.Integer, nullable=False)


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    def send_confirmation_email(self):
        self.activated = True

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
