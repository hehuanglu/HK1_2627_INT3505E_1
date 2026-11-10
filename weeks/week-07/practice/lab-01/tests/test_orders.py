from sqlalchemy import event

from product_api.extensions import db
from product_api.models import Order, OrderItem, Product


def add_product(app, *, sku="PEN-001", name="Bút chì", price_cents=5000):
    with app.app_context():
        product = Product(
            sku=sku,
            name=name,
            price_cents=price_cents,
            qty_in_stock=10,
        )
        db.session.add(product)
        db.session.commit()
        return product.id


def test_post_order_creates_association_items_and_price_snapshot(app, client):
    product_id = add_product(app)

    response = client.post(
        "/api/v1/orders",
        json={
            "customer_name": "Nguyễn An",
            "items": [{"product_id": product_id, "quantity": 2}],
        },
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["customer_name"] == "Nguyễn An"
    assert body["items"][0]["product_id"] == product_id
    assert body["items"][0]["quantity"] == 2
    assert body["items"][0]["unit_price_cents"] == 5000

    with app.app_context():
        assert db.session.scalar(db.select(db.func.count()).select_from(Order)) == 1
        assert db.session.scalar(db.select(db.func.count()).select_from(OrderItem)) == 1


def test_get_orders_eager_loads_items_and_products(app, client):
    first_id = add_product(app)
    second_id = add_product(
        app, sku="PEN-002", name="Bút mực", price_cents=9000
    )
    with app.app_context():
        products = {p.id: p for p in db.session.scalars(db.select(Product)).all()}
        first_order = Order(customer_name="Khách A")
        first_order.items = [
            OrderItem(product=products[first_id], quantity=1, unit_price_cents=5000),
            OrderItem(product=products[second_id], quantity=3, unit_price_cents=9000),
        ]
        second_order = Order(customer_name="Khách B")
        second_order.items = [
            OrderItem(product=products[first_id], quantity=2, unit_price_cents=5000)
        ]
        db.session.add_all([first_order, second_order])
        db.session.commit()

    statements = []

    def record_query(_conn, _cursor, statement, _parameters, _context, _many):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    with app.app_context():
        event.listen(db.engine, "before_cursor_execute", record_query)
    try:
        response = client.get("/api/v1/orders")
    finally:
        with app.app_context():
            event.remove(db.engine, "before_cursor_execute", record_query)

    assert response.status_code == 200
    orders = response.get_json()
    assert len(orders) == 2
    assert [item["product"]["name"] for item in orders[0]["items"]] == [
        "Bút chì",
        "Bút mực",
    ]
    # One query for orders and one select-in query for all order items/products.
    assert len(statements) == 2
