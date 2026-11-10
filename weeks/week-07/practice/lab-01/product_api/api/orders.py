from flask import Blueprint, request
from marshmallow import ValidationError

from ..errors import ValidationFailed
from ..schemas import OrderIn, OrderOut
from ..services.orders import create_order, get_order, list_orders


orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")
order_in = OrderIn()
order_out = OrderOut()


def load_order():
    try:
        return order_in.load(request.get_json())
    except ValidationError as error:
        raise ValidationFailed(str(error.messages)) from error


@orders_bp.post("")
def create_order_resource():
    order = create_order(load_order())
    return order_out.dump(order), 201


@orders_bp.get("")
def list_order_resources():
    return order_out.dump(list_orders(), many=True), 200


@orders_bp.get("/<int:order_id>")
def get_order_resource(order_id):
    return order_out.dump(get_order(order_id)), 200
