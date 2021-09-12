from uuid import UUID
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., example="Zézé")
    cpf: str = Field(..., example="862.851.840-11")
    email: str = Field(..., example="email@email.com")
    phone_number: str = Field(..., example="21988002299")

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    id: UUID
    name: str
    cpf: str
    email: str
    phone_number: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
