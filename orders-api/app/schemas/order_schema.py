from uuid import UUID
from pydantic import BaseModel, condecimal, conint, Field
from sqlalchemy.dialects.postgresql import MONEY

from app.schemas.user_schema import User


class Order(BaseModel):
    item_description: str = Field(..., example="Descrição do pedido...")
    item_quantity: conint(gt=0, strict=True) = Field(..., example=1)
    item_price: condecimal(ge=0, decimal_places=2) = Field(..., example=1.99)
    user_id: UUID

    class Config:
        orm_mode = True


class OrderInfo(BaseModel):
    id: UUID
    item_description: str
    item_quantity: int
    item_price: str
    total_value: str
    created_at: str
    updated_at: str
    user: User

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    id: UUID
    item_description: str
    item_quantity: int
    item_price: str
    total_value: str
    created_at: str
    updated_at: str
    user_id: UUID

    class Config:
        orm_mode = True