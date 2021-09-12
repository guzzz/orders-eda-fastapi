import uuid

from sqlalchemy.dialects.postgresql import UUID, MONEY
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from app.config.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True)
    item_description = Column(String)
    item_quantity = Column(Integer)
    item_price = Column(MONEY)
    total_value = Column(MONEY)
    created_at = Column(String)
    updated_at = Column(String)
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), index=True)

    user = relationship("User", back_populates="orders")
