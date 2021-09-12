import uuid

from app.tests.db_test import client
from app.models.user import User
from app.utils.dates import now


def test_create_user_unit():
    user = User(
        id=uuid.uuid4(),
        name="Salah",
        cpf="123131231",
        email="email@email.com",
        phone_number="21999999999",
        created_at=now(),
        updated_at=now()
    )
    assert user.name == "Salah"
