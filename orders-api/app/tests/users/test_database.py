from app.repositories.user_repository import UserRepository
from app.tests.db_test import DB, client

user_repository = UserRepository()


def create_user():
    user = {
        "name": "Vini Jr.",
        "cpf": "gAAAAABhN8PWIzeJHofJX_Gn9edH-yZ1GmBp5PpNJtmFy2lMYVeNUfzMIjPl3UWET3DZGdw0-p1XaL9wnW2J-uQO6WrCc2FIHw==",
        "email": "gAAAAABhN8PWLD_RxWOQ0SYOWFPSPsea-_i7zeIf1B6dJSRQA9OfXpVwJtfUvVgoXPm9S3onF80UEP6_1aOgskLgETXoMaLDcw==",
        "phone_number": "gAAAAABhN8PWKw0zQCV4JPv7CHVeQq6mExusa-HBaUTvyr0LQN2oz-mKi00NjUFFo_9OglaHnY8di_smQvWyI1Z4WQrz_Hkdjw=="
    }
    return user_repository.create(DB, user)
    

def test_user_db_create():
    user_created = create_user()
    assert user_created.name == "Vini Jr."

def test_user_db_read():
    created = create_user()
    retrieved = user_repository.retrieve(DB, created.id)
    assert created.id == retrieved.id

def test_user_db_update():
    created = create_user()
    user = {
        "name": "Neymar Jr.",
        "cpf": "gAAAAABhN8PWIzeJHofJX_Gn9edH-yZ1GmBp5PpNJtmFy2lMYVeNUfzMIjPl3UWET3DZGdw0-p1XaL9wnW2J-uQO6WrCc2FIHw==",
        "email": "gAAAAABhN8PWLD_RxWOQ0SYOWFPSPsea-_i7zeIf1B6dJSRQA9OfXpVwJtfUvVgoXPm9S3onF80UEP6_1aOgskLgETXoMaLDcw==",
        "phone_number": "gAAAAABhN8PWKw0zQCV4JPv7CHVeQq6mExusa-HBaUTvyr0LQN2oz-mKi00NjUFFo_9OglaHnY8di_smQvWyI1Z4WQrz_Hkdjw=="
    }
    user_updated = user_repository.update(DB, created.id, user)
    assert user_updated.name == "Neymar Jr."

def test_user_db_delete():
    created = create_user()
    user_repository.delete(DB, created.id)
    retrieved = user_repository.retrieve(DB, created.id)
    assert retrieved == None
