from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from .schemas import ProductSchema, ProductInSchema
from .models import Product
try:
    from ..extensions import db
except (ImportError, ValueError):
    from extensions import db
blp = Blueprint("products", __name__, url_prefix="/products")

class ProductList(MethodView):
    @blp.arguments(ProductInSchema)
    @blp.response(201, ProductSchema)
    def post(self, data):
        p = Product(**data)
        db.session.add(p)
        db.session.commit()
        return p

    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return db.session.execute(db.select(Product)).scalars().all()

blp.add_url_rule("/", view_func=ProductList.as_view("product_list"))