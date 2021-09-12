from app.tests.users.test_database import create_user
from app.tests.db_test import client


def test_create_user():
    user = {
        "name": "Ronaldo",
        "cpf": "54176357070",
        "email": "email@email.com",
        "phone_number": "21988747724"
    }
    response = client.post("/v0/users/", json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Ronaldo"
    assert "id" in data

def test_list_users():
    response = client.get(f"/v0/users")
    assert response.status_code == 200

def test_retrieve_user_invalid_uuid_error():
    response = client.get("/v0/users/1111111111111")
    assert response.status_code == 400

def test_retrieve_user_not_found_error():
    response = client.get("/v0/users/8621bd75-bb20-4978-bf63-02575fe3468c")
    assert response.status_code == 404

def test_retrieve_valid_id():
    user = create_user()
    uuid = user.id
    response = client.get(f"/v0/users/{uuid}")
    assert response.status_code == 200

def test_update_user():
    user = create_user()
    uuid = user.id
    response = client.get(f"/v0/users/{uuid}")
    user_json = response.json()
    update_json = {
        "name": "Ronaldinho Gaúcho",
        "cpf": user_json["cpf"],
        "email": user_json["email"],
        "phone_number": user_json["phone_number"]
    }
    response = client.put(f"/v0/users/{uuid}", json=update_json)
    r = response.json()
    assert r["name"] == "Ronaldinho Gaúcho"
    assert response.status_code == 200

def test_delete_user():
    user = create_user()
    uuid = user.id
    response = client.delete(f"/v0/users/{uuid}")
    assert response.status_code == 204

def test_delete_user_fail():
    response = client.delete(f"/v0/users/8621bd75-bb20-4978-bf63-02575fe3468c")
    assert response.status_code == 404
