from aula19.ext.database import db
from aula19.ext.models import Product

def create_db():
    db.create_all()

def drop_db():
    db.drop_all()

def populate_db():
    p = Product()
    db.session.add(p)
    db.session.commit()
    return Product.query.all()
