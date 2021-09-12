from app.tests.db_test import DB, client
from app.repositories.order_repository import OrderRepository
from app.repositories.user_repository import UserRepository
from app.tests.users.test_database import create_user

order_repository = OrderRepository()


def create_order():
    user = create_user()
    uuid = user.id
    order = {
        "item_description": "Description Test",
        "item_quantity": 1,
        "item_price": 10.15,
        "total_value": 10.15,
        "user_id": str(uuid)
    }
    return order_repository.create(DB, order)

def create_order_plus_user():
    user = create_user()
    uuid = user.id
    order = {
        "item_description": "Description Test",
        "item_quantity": 1,
        "item_price": 10.15,
        "total_value": 10.15,
        "user_id": str(uuid)
    }
    return order_repository.create(DB, order), str(uuid)
    

def test_order_create():
    order_created = create_order()
    assert order_created.item_description == "Description Test"

def test_order_db_read():
    created = create_order()
    retrieved = order_repository.retrieve(DB, created.id)
    assert created.id == retrieved.id

def test_order_db_update():
    created = create_order()
    order = {
        "item_description": "NEW DESCRIPTION",
        "item_quantity": created.item_quantity,
        "item_price": created.item_price,
        "total_value": created.total_value,
        "user_id": created.user_id
    }
    order_updated = order_repository.update(DB, created.id, order)
    assert order_updated.item_description == "NEW DESCRIPTION"


def test_order_db_delete():
    created = create_order()
    order_repository.delete(DB, created.id)
    retrieved = order_repository.retrieve(DB, created.id)
    assert retrieved == None
