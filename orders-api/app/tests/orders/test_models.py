import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.models.user import Order
from app.utils.dates import now

client = TestClient(app)


def test_create_order_unit():
    order = Order(
        id=uuid.uuid4(),
        item_description="Pedido 1",
        item_quantity=1,
        item_price=10.15,
        total_value=10.15,
        user_id="8621bd75-bb20-4978-bf63-02575fe3468c",
        created_at=now(),
        updated_at=now()
    )
    assert order.item_description == "Pedido 1"
