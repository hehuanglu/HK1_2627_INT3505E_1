from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload

from ..errors import Conflict, NotFound
from ..extensions import db
from ..models import Order, OrderItem, Product


def create_order(data):
    items = data["items"]
    product_ids = [item["product_id"] for item in items]
    if len(set(product_ids)) != len(product_ids):
        raise Conflict("Mỗi sản phẩm chỉ được xuất hiện một lần trong đơn hàng.")

    products = db.session.scalars(
        select(Product).where(
            Product.id.in_(product_ids), Product.archived.is_(False)
        )
    ).all()
    by_id = {product.id: product for product in products}
    missing = [product_id for product_id in product_ids if product_id not in by_id]
    if missing:
        raise NotFound(f"Không tìm thấy sản phẩm: {missing[0]}.")

    order = Order(customer_name=data["customer_name"])
    order.items = [
        OrderItem(
            product=by_id[item["product_id"]],
            quantity=item["quantity"],
            unit_price_cents=by_id[item["product_id"]].price_cents,
        )
        for item in items
    ]
    db.session.add(order)
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise Conflict("Đơn hàng vi phạm ràng buộc dữ liệu.") from error
    return order


def list_orders():
    statement = (
        select(Order)
        .options(selectinload(Order.items).joinedload(OrderItem.product))
        .order_by(Order.id)
    )
    return db.session.scalars(statement).all()


def get_order(order_id):
    statement = (
        select(Order)
        .options(selectinload(Order.items).joinedload(OrderItem.product))
        .where(Order.id == order_id)
    )
    order = db.session.scalar(statement)
    if order is None:
        raise NotFound("Không tìm thấy đơn hàng.")
    return order
