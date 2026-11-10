from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from ..errors import Conflict, NotFound, ValidationFailed
from ..extensions import db
from ..models import Product
from ..schemas import PaginationQuery, ProductIn, ProductOut, ProductPatch, ReserveIn


products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")
product_out = ProductOut()


def load_json(schema):
    try:
        return schema.load(request.get_json())
    except ValidationError as error:
        raise ValidationFailed(str(error.messages)) from error


def get_active_product(product_id):
    product = db.session.scalar(
        db.select(Product).where(
            Product.id == product_id,
            Product.archived.is_(False),
        )
    )
    if product is None:
        raise NotFound("Không tìm thấy sản phẩm.")
    return product


@products_bp.get("")
def list_products():
    try:
        pagination = PaginationQuery().load(request.args)
    except ValidationError as error:
        raise ValidationFailed(str(error.messages)) from error

    page = pagination["page"]
    size = pagination["size"]
    active_products = db.select(Product).where(Product.archived.is_(False))
    products = db.session.scalars(
        active_products.order_by(Product.id)
        .offset((page - 1) * size)
        .limit(size)
    ).all()
    total = db.session.scalar(
        db.select(db.func.count())
        .select_from(Product)
        .where(Product.archived.is_(False))
    )
    return {
        "items": product_out.dump(products, many=True),
        "page": page,
        "size": size,
        "total": total,
    }, 200


@products_bp.get("/<int:product_id>")
def get_product(product_id):
    return product_out.dump(get_active_product(product_id)), 200


@products_bp.post("")
def create_product():
    product = Product(**load_json(ProductIn()))
    db.session.add(product)
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise Conflict("sku đã tồn tại.") from error
    return product_out.dump(product), 201


@products_bp.post("/<int:product_id>/reserve")
def reserve_product(product_id):
    body = load_json(ReserveIn())
    product = get_active_product(product_id)
    if product.qty_in_stock < body["qty"]:
        raise Conflict("Không đủ hàng trong kho.")

    product.qty_in_stock -= body["qty"]
    db.session.commit()
    return product_out.dump(product), 200


@products_bp.patch("/<int:product_id>")
def patch_product(product_id):
    changes = load_json(ProductPatch())
    if not changes:
        raise ValidationFailed("Cần cung cấp ít nhất một trường để cập nhật.")

    product = get_active_product(product_id)
    for field, value in changes.items():
        setattr(product, field, value)
    db.session.commit()
    return product_out.dump(product), 200


@products_bp.delete("/<int:product_id>")
def delete_product(product_id):
    product = get_active_product(product_id)
    product.archived = True
    db.session.commit()
    return "", 204
