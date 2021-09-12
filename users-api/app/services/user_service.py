import json
import copy
import uuid

from structlog import get_logger
from fastapi.encoders import jsonable_encoder

from app.serializers.user_serializer import user_serializer, users_serializer
from app.services.cryptography_service import CryptographyService
from app.repositories.user_repository import UserRepository
from app.services.redis_service import RedisService
from app.producer import publish
from app.utils.dates import now

user_repository = UserRepository()
redis_service = RedisService()
cryptography_service = CryptographyService()
log = get_logger()


class UserService:

    def __init__(self):
        self.database = user_repository
        self.mem_database = redis_service
        self.cryptographer = cryptography_service

    def retrieve(self, uuid):
        log.info("[RETRIEVE - user] Started retrieve service...")
        log.info("[CACHE - user] Searching in cache...")
        obj_from_mem = self.mem_database.get_value(str(uuid))
        if obj_from_mem:
            obj_json = json.loads(obj_from_mem.decode("UTF-8"))
            user = self.cryptographer.decrypt_user(obj_json)
        else:
            log.info("[CACHE - user] Not found...")
            user = self.retrieve_from_db(uuid)
        return user

    def retrieve_from_db(self, id, uuid=True):
        log.info("[DB - user] Searching in database...")
        obj_from_db = self.database.retrieve(id, uuid)
        if obj_from_db:
            user = user_serializer(obj_from_db)
            user_copy = copy.deepcopy(user)
            user_encrypted = self.cryptographer.encrypt_user(user_copy)
            user_to_store = json.dumps(user_encrypted).encode('utf-8')
            self.mem_database.set_value(user_copy["id"], user_to_store)
        else:
            log.info("[DB - user] Not found...")
            user = None
        return user

    def list(self, page, limit):
        log.info("[LIST - user] Started list service...")
        return users_serializer(self.database.list(page, limit))

    def create(self, user_obj):
        log.info("[CREATE - user] Started creation service...")
        user = jsonable_encoder(user_obj)
        user["id"] = uuid.uuid4()
        user["created_at"] = now()
        user["updated_at"] = now()
        user = self.cryptographer.encrypt_user(user)
        result = self.database.create(user)
        del user["_id"]
        publish(action="create", body=user)
        return self.retrieve_from_db(result.inserted_id, uuid=False)

    def update(self, uuid, user_obj):
        log.info("[UPDATE] Start update...")
        user = jsonable_encoder(user_obj)
        user["updated_at"] = now()
        user = self.cryptographer.encrypt_user(user)
        result = self.database.update(uuid, user)
        if result:
            self.mem_database.delete_value(str(uuid))
            publish(action="update", body=user, user_id=str(uuid))
            return self.retrieve_from_db(uuid)
        else:
            log.info("[UPDATE - user] Not found...")
            return False

    def delete(self, uuid):
        log.info("[DELETE - user] Started delete service...")
        result = self.database.delete(uuid)
        if result:
            self.mem_database.delete_value(str(uuid))
            publish(action="delete", user_id=str(uuid))
            return True
        else:
            log.info("[DELETE - user] Not found...")
            return False
