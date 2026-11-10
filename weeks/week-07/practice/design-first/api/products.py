from flask import jsonify

from models import Product
from extensions import db


def list_products():
    products = db.session.execute(db.select(Product)).scalars().all()
    return jsonify([product.to_dict() for product in products]), 200


def create_product(body):
    product = Product(**body)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201
