from flask import jsonify
from aula18.ext.models import Product, Client
from flask_restful import Resource, abort, reqparse
from aula18.ext.database import db

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

    def get(self):
        products = Product.query.all() or abort(404, description="Resource not found")
        return {"products": [product.to_dict() for product in products]}, 201

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

    def get(self, product_id):
        product = Product.query.filter_by(id=product_id).first() or abort(
            404, description=f"Resource id {product_id} not found")
        return product.to_dict(), 201

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

    def get(self, client_id):
        clients = Client.query.all() or abort(404, description="Resource not found")
        return {"clients": [client.to_dict() for client in clients]}

    def post(self, client_id):
        args = self.reqparse.parse_args()
        client = Client(**args)
        db.session.add(client)
        db.session.commit()
        return jsonify({"success": True, "response": "client added"})

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

    def delete(self, client_id):
        client = Client.query.filter_by(id=client_id).first() or abort(
            404, description=f"Resource id {client_id} not found")
        db.session.delete(client)
        db.session.commit()
        return {"success": True, "response": "client deleted"}, 201
