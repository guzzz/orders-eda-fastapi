from app.utils.dates import now
from pydantic import BaseModel, EmailStr, validator, StrictStr, Field
from pycpfcnpj import cpfcnpj


class User(BaseModel):
    name: StrictStr = Field(..., example="Zézé")
    cpf: str = Field(..., example="862.851.840-11")
    email: EmailStr = Field(..., example="email@email.com")
    phone_number: str = Field(..., example="21988002299")

    @validator('cpf')
    def cpf_validation(cls, value):
        clean_cpf = value.replace(".", "").replace("-", "").strip()
        valid_cpf = cpfcnpj.validate(clean_cpf)
        if valid_cpf:
            return clean_cpf
        else:
            raise ValueError('Invalid CPF')

    @validator('phone_number')
    def phone_number_validation(cls, value):
        clean_phone_number = value
        remove_characters = ["(", ")", "-", "+", " "]
        for character in remove_characters:
            clean_phone_number = clean_phone_number.replace(character, "")
        digits = len(clean_phone_number)
        if digits == 10:
            return clean_phone_number
        elif digits == 11 and clean_phone_number[2] == "9":
            return clean_phone_number
        elif digits in (13, 12) and clean_phone_number[0] == "5" and clean_phone_number[1] == "5":
            clean_phone_number = clean_phone_number[2:]
            return clean_phone_number
        elif digits == 11 and clean_phone_number[2] != "9":
            raise ValueError('Invalid Phone Number. Cellphones should begin with 9 digit after DDD.')
        else:
            raise ValueError('Invalid Phone Number. Remember Correct phone number must contain DDD and number.')
