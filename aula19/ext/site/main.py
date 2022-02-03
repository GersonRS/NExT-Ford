from flask import Blueprint, render_template
from aula19.ext.models import Product, Category

bp = Blueprint('site', __name__, template_folder="templates")


@bp.route('/product/index', methods=['GET'])
def product_index():
    products = Product.query.all()
    return render_template('product/index.html', products=products)


@bp.route('/product/create')
def product_create():
    categories = Category.query.all()
    return render_template('product/create.html', categories=categories)
