from datetime import datetime
from flask import jsonify
from aula19.ext.models import Product, Client, User
from flask_restful import Resource, abort, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from aula19.ext.database import db


class ProductListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', required=False, type=str,
                                   help='mande algum nome')
        self.reqparse.add_argument('price', required=False, type=float,
                                   help='mande algum preço', default=0.0)
        self.reqparse.add_argument(
            'category_id', required=False, type=int, default=1)
        super(ProductListAPI, self).__init__()

    @jwt_required()
    def get(self):
        products = Product.query.all() or abort(404, description="Resource not found")
        return {"products": [product.to_dict() for product in products]}, 201

    @jwt_required()
    def post(self):
        args = self.reqparse.parse_args()
        product = Product(name=args.name, price=args.price,
                          category_id=args.category_id)
        db.session.add(product)
        db.session.commit()
        return jsonify({"success": True, "response": "product added"})


class ProductAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', required=False, type=str,
                                   help='mande algum nome')
        self.reqparse.add_argument('price', required=False, type=float,
                                   help='mande algum preço', default=0.0)
        self.reqparse.add_argument(
            'category_id', required=False, type=int, default=1)
        super(ProductListAPI, self).__init__()

    @jwt_required()
    def get(self, product_id):
        product = Product.query.filter_by(id=product_id).first() or abort(
            404, description=f"Resource id {product_id} not found")
        return product.to_dict(), 201

    @jwt_required()
    def put(self, product_id):
        args = self.reqparse.parse_args()

        product = Product.query.filter_by(id=product_id).first() or abort(
            404, description=f"Resource id {product_id} not found")

        if args.name:
            product.name = args.name
        if args.price:
            product.price = args.price
        if args.category_id:
            product.category_id = args.category_id

        db.session.add(product)
        db.session.commit()
        return {"success": True, "response": "product edited"}, 201

    @jwt_required()
    def delete(self, product_id):
        product = Product.query.filter_by(id=product_id).first() or abort(
            404, description=f"Resource id {product_id} not found")
        db.session.delete(product)
        db.session.commit()
        return {"success": True, "response": "product deleted"}, 201


class ClientAPI(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='recurso não enviado, prfv mande um nome')
        self.reqparse.add_argument('address', type=str, required=True,
                                   help='recurso não enviado, prfv mande um endereço')
        self.reqparse.add_argument('telephone_fix', type=str, required=True,
                                   help='recurso não enviado, prfv mande um telefone fixo')
        self.reqparse.add_argument('telephone_celular', type=str, required=True,
                                   help='recurso não enviado, prfv mande um telefone celular')
        self.reqparse.add_argument('status', type=str, required=True,
                                   help='recurso não enviado, prfv mande um status')
        self.reqparse.add_argument('credit_limit', type=str, required=True,
                                   help='recurso não enviado, prfv mande um limite de credito')
        super(ClientAPI, self).__init__()

    @jwt_required()
    def get(self, client_id):
        clients = Client.query.all() or abort(404, description="Resource not found")
        return {"clients": [client.to_dict() for client in clients]}

    @jwt_required()
    def post(self, client_id):
        args = self.reqparse.parse_args()
        client = Client(**args)
        db.session.add(client)
        db.session.commit()
        return jsonify({"success": True, "response": "client added"})

    @jwt_required()
    def put(self, client_id):
        client = Client.query.filter_by(id=client_id).first() or abort(
            404, description=f"Resource id {client_id} not found")

        args = self.reqparse.parse_args()
        if args.name:
            client.name = args.name
        if args.address:
            client.address = args.address
        if args.telephone_fix:
            client.telephone_fix = args.telephone_fix
        if args.telephone_celular:
            client.telephone_celular = args.telephone_celular
        if args.status:
            client.status = args.status
        if args.credit_limit:
            client.credit_limit = args.credit_limit

        db.session.add(client)
        db.session.commit()
        return {"success": True, "response": "client edited"}, 201

    @jwt_required()
    def delete(self, client_id):
        client = Client.query.filter_by(id=client_id).first() or abort(
            404, description=f"Resource id {client_id} not found")
        db.session.delete(client)
        db.session.commit()
        return {"success": True, "response": "client deleted"}, 201


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True,
                       help="The field 'login' cannot be left blank.")
atributos.add_argument('password', type=str, required=True,
                       help="The field 'password' cannot be left blank.")
atributos.add_argument('email', type=str)
atributos.add_argument('activated', type=bool)


class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return {"message": "The field 'email' cannot be left blank."}, 400

        if User.find_by_email(dados['email']):
            return {"message": "The email '{}' already exists.".format(dados['email'])}, 400

        if User.find_by_login(dados['login']):
            # Bad Request
            return {"message": "The login '{}' already exists.".format(dados['login'])}, 400

        user = User(**dados)
        user.activated = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            return {'message': 'An internal server error has ocurred.'}, 500
        return {'message': 'User created successfully!'}, 201  # Created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = User.find_by_login(dados['login'])

        if user and safe_str_cmp(user.password, dados['password']):
            token_de_acesso = create_access_token(identity=user.id)
            return {'access_token': token_de_acesso}, 200
        # Unauthorized
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_jwt_identity()['jti']  # JWT Token Identifier
        # BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
