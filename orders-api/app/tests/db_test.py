from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import user, order
from app.config.database import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgresuser:postgrespwd@postgres-test/ordersdbtest"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

user.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
DB = TestingSessionLocal()
