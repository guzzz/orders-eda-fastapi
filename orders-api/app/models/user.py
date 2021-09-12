import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.order import Order


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    cpf = Column(String)
    email = Column(String)
    phone_number = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

    orders = relationship(Order, back_populates="user", cascade="all, delete", passive_deletes=True)
