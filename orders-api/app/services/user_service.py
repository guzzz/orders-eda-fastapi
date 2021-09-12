import uuid
import json
import copy

from structlog import get_logger
from fastapi.encoders import jsonable_encoder

from app.services.cryptography_service import CryptographyService
from app.serializers.user_serializer import users_serializer, user_serializer_clean
from app.repositories.user_repository import UserRepository
from app.services.redis_service import RedisService
from app.utils.dates import now

cryptography_service = CryptographyService()
user_repository = UserRepository()
redis_service = RedisService()
log = get_logger()


class UserService:

    def __init__(self):
        self.database = user_repository
        self.mem_database = redis_service
        self.cryptographer = cryptography_service

    def retrieve(self, db, uuid):
        log.info("[RETRIEVE - user] Started retrieve service...")
        log.info("[CACHE - user] Searching in cache...")
        obj_from_mem = self.mem_database.get_value(str(uuid))
        if obj_from_mem:
            obj_json = json.loads(obj_from_mem.decode("UTF-8"))
            user = self.cryptographer.decrypt_user(obj_json)
        else:
            log.info("[CACHE - user] Not found...")
            user = self.retrieve_from_db(db, uuid)

        if user:
            user = user_serializer_clean(user)
        return user

    def retrieve_from_db(self, db, uuid):
        log.info("[DB - user] Searching in database...")
        obj_from_db = self.database.retrieve(db, uuid)
        if obj_from_db:
            user_encrypted = jsonable_encoder(obj_from_db)
            user_to_store = json.dumps(user_encrypted).encode('utf-8')
            self.mem_database.set_value(user_encrypted["id"], user_to_store)
            user = self.cryptographer.decrypt_user(user_encrypted)
        else:
            log.info("[DB - user] Not found...")
            user = None
        return user
    
    def list(self, db, page, limit):
        log.info("[LIST - user] Started list service...")
        users_list = self.database.list(db, page, limit)
        return users_serializer(users_list)

    def create(self, db, user_obj):
        log.info("[CREATE - user] Started creation service...")
        user = jsonable_encoder(user_obj)
        user["id"] = uuid.uuid4()
        user["created_at"] = now()
        user["updated_at"] = now()

        user_copy = copy.deepcopy(user)
        user_encrypted = self.cryptographer.encrypt_user(user)
        self.database.create(db, user_encrypted)
        
        return user_serializer_clean(user_copy)

    def update(self, db, uuid, user_obj):
        log.info("[UPDATE - user] Started update service...")
        user = jsonable_encoder(user_obj)
        user["updated_at"] = now()
        user = self.cryptographer.encrypt_user(user)
        self.mem_database.delete_value(str(uuid))
        result = self.database.update(db, uuid, user)
        if result:
            user = self.retrieve_from_db(db, uuid)
            if user:
                user = user_serializer_clean(user)
                return user
        else:
            log.info("[UPDATE - user] Not found...")
            return False

    def delete(self, db, uuid):
        log.info("[DELETE - user] Started delete service...")
        result = self.database.delete(db, uuid)
        if result:
            self.mem_database.delete_value(str(uuid))
            return True
        else:
            log.info("[DELETE - user] Not found...")
            return False

    def eda_create(self, db, user_obj):
        log.info("[CREATE] Start event driven creation...")
        user = jsonable_encoder(user_obj)
        self.database.eda_create(db, user)

    def eda_update(self, db, user_id, user_obj):
        log.info("[UPDATE] Start event driven update...")
        user = jsonable_encoder(user_obj)
        self.mem_database.delete_value(user_id)
        self.database.eda_update(db, user_id, user)

    def eda_delete(self, db, user_id):
        log.info("[DELETE] Start event driven deletion...")
        self.database.eda_delete(db, user_id)
        self.mem_database.delete_value(user_id)
