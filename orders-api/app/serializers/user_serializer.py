from app.services.cryptography_service import CryptographyService

cryptography_service = CryptographyService()


def user_serializer_clean(user):
    return {
        "id": str(user["id"]),
        "name": user["name"],
        "email": user["email"],
        "cpf": cpf_with_punctuation(user["cpf"]),
        "phone_number": phone_number_organized(user["phone_number"]),
        "created_at": str(user["created_at"]),
        "updated_at": str(user["updated_at"])
    }

def user_serializer(user):
    return {
        "id": str(user.id),
        "name": user.name,
        "email": cryptography_service.decrypt(user.email),
        "cpf": cpf_with_punctuation(cryptography_service.decrypt(user.cpf)),
        "phone_number": phone_number_organized(cryptography_service.decrypt(user.phone_number)),
        "created_at": str(user.created_at),
        "updated_at": str(user.updated_at)
    }


def users_serializer(users_list):
    return [user_serializer(user) for user in users_list]


def cpf_with_punctuation(cpf):
    return '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])


def phone_number_organized(phone_number):
    digits = len(phone_number)
    if digits == 10:
        return '({}) {}-{}'.format(phone_number[:2], phone_number[2:6], phone_number[6:])
    else:
        return '({}) {}-{}'.format(phone_number[:2], phone_number[2:7], phone_number[7:])
