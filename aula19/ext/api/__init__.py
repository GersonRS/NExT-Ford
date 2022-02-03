from flask import Blueprint
from flask_restful import Api

from .resource import ProductAPI, ProductListAPI, ClientAPI, UserLogin, UserLogout, UserRegister


bp = Blueprint("restapi", __name__, url_prefix="/api/v1")

api = Api(bp)

def init_app(app):
    api.add_resource(ProductListAPI, "/product/")
    api.add_resource(ProductAPI,  "/product/<int:product_id>")
    api.add_resource(ClientAPI,  "/client/", "/client/<int:client_id>")
    api.add_resource(UserRegister, '/cadastro')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    app.register_blueprint(bp)
