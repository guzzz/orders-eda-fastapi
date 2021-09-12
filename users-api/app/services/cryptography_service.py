import os

from structlog import get_logger
from cryptography.fernet import Fernet

log = get_logger()
CRYPTOGRAPHY_KEY: str = os.getenv("CRYPTOGRAPHY_KEY")


class CryptographyService:

    def __init__(self):
        self.fernet = Fernet(CRYPTOGRAPHY_KEY)

    def encrypt(self, info):
        info_bytes = info.encode()
        info_encrypted = self.fernet.encrypt(info_bytes)
        info_str = info_encrypted.decode("UTF-8")
        return info_str

    def decrypt(self, info):
        info_bytes = info.encode()
        info_decrypted = self.fernet.decrypt(info_bytes)
        info_str = info_decrypted.decode("UTF-8")
        return info_str

    def encrypt_user(self, user):
        log.info("[ENCRYPT] Encrypt USER")
        user["cpf"] = self.encrypt(user.get("cpf"))
        user["email"] = self.encrypt(user.get("email"))
        user["phone_number"] = self.encrypt(user.get("phone_number"))
        return user

    def decrypt_user(self, user):
        log.info("[DECRYPT] Decrypt USER")
        user["cpf"] = self.decrypt(user.get("cpf"))
        user["email"] = self.decrypt(user.get("email"))
        user["phone_number"] = self.decrypt(user.get("phone_number"))
        return user
