from app.tests.orders.test_database import create_order, create_order_plus_user
from app.tests.users.test_database import create_user
from app.tests.db_test import client


def test_create_order():
    user = create_user()
    uuid = user.id
    order = {
        "item_description": "Description Test 1",
        "item_quantity": 1,
        "item_price": 10.15,
        "user_id": str(uuid)
    }
    response = client.post("/v0/orders/", json=order)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["item_description"] == "Description Test 1"
    assert "id" in data

def test_list_orders():
    response = client.get(f"/v0/orders")
    assert response.status_code == 200

def test_retrieve_order_invalid_uuid_error():
    response = client.get("/v0/orders/1111111111111")
    assert response.status_code == 400

def test_retrieve_order_not_found_error():
    response = client.get("/v0/orders/8621bd75-bb20-4978-bf63-02575fe3468c")
    assert response.status_code == 404

def test_retrieve_valid_id():
    order = create_order()
    uuid = order.id
    response = client.get(f"/v0/orders/{uuid}")
    assert response.status_code == 200

def test_update_order():
    order, user_id = create_order_plus_user()
    uuid = order.id
    response = client.get(f"/v0/orders/{uuid}")
    order_json = response.json()
    update_json = {
        "item_description": "Description Test 2",
        "item_quantity": 10,
        "item_price": 1.00,
        "user_id": user_id
    }
    response = client.put(f"/v0/orders/{uuid}", json=update_json)
    r = response.json()
    print(r)
    print(response.status_code)
    assert r["item_description"] == "Description Test 2"
    assert response.status_code == 200

def test_delete_order():
    order = create_order()
    uuid = order.id
    response = client.delete(f"/v0/orders/{uuid}")
    assert response.status_code == 204

def test_delete_order_fail():
    response = client.delete(f"/v0/orders/8621bd75-bb20-4978-bf63-02575fe3468c")
    assert response.status_code == 404
