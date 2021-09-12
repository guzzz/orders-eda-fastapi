import uuid
import json
import copy

from decimal import Decimal
from structlog import get_logger
from fastapi.encoders import jsonable_encoder

from app.services.cryptography_service import CryptographyService
from app.repositories.order_repository import OrderRepository
from app.services.user_service import UserService
from app.services.redis_service import RedisService
from app.utils.dates import now

cryptography_service = CryptographyService()
order_repository = OrderRepository()
redis_service = RedisService()
user_service = UserService()
log = get_logger()


class OrderService:

    def __init__(self):
        self.database = order_repository
        self.mem_database = redis_service
        pass

    def retrieve(self, db, uuid):
        log.info("[RETRIEVE - order] Started retrieve service...")
        log.info("[CACHE - order] Searching in cache...")
        obj_from_mem = self.mem_database.get_value(str(uuid))
        if obj_from_mem:
            order = json.loads(obj_from_mem.decode("UTF-8"))
            order["user"] = cryptography_service.decrypt_user(order["user"])
        else:
            log.info("[CACHE - order] Not found...")
            order = self.retrieve_from_db(db, uuid)
        return order

    def retrieve_from_db(self, db, uuid):
        log.info("[DB - order] Searching in database...")
        obj_from_db = self.database.retrieve(db, uuid)
        if obj_from_db:
            order = jsonable_encoder(obj_from_db)
            user = user_service.retrieve(db, order["user_id"])

            user_copy = copy.deepcopy(user)
            user_encrypted = cryptography_service.encrypt_user(user_copy)
            order["user"] = user_encrypted
            order_to_store = json.dumps(order).encode('utf-8')
            self.mem_database.set_value(order["id"], order_to_store)

            order["user"] = user
        else:
            log.info("[DB - order] Not found...")
            order = None
        return order
    
    def list(self, db, page, limit, user_id_filter):
        log.info("[LIST - order] Started list service...")
        return self.database.list(db, page, limit, user_id_filter)

    def create(self, db, order_obj):
        log.info("[CREATE - order] Started creation service...")
        order = jsonable_encoder(order_obj)
        total = self.calculate_total_value(order["item_quantity"], order["item_price"])
        order["id"] = uuid.uuid4()
        order["total_value"] = total

        order_created = self.database.create(db, order)
        order_serialized = jsonable_encoder(order_created)

        user = user_service.retrieve(db, order_created.user_id)
        del order_serialized["user_id"]
        order_serialized["user"] = user
        return order_serialized

    def update(self, db, uuid, order_obj):
        log.info("[UPDATE - order] Started update service...")
        order = jsonable_encoder(order_obj)
        total = self.calculate_total_value(order["item_quantity"], order["item_price"])
        order["total_value"] = total
        self.mem_database.delete_value(str(uuid))
        result = self.database.update(db, uuid, order)
        if result:
            return self.retrieve_from_db(db, uuid)
        else:
            log.info("[UPDATE - order] Not found...")
            return False

    def delete(self, db, uuid):
        log.info("[DELETE - order] Started delete service...")
        result = self.database.delete(db, uuid)
        if result:
            self.mem_database.delete_value(str(uuid))
            return True
        else:
            log.info("[DELETE - order] Not found...")
            return False

    def calculate_total_value(self, quantity, price):
        TWOPLACES = Decimal(10) ** -2
        return Decimal(quantity*price).quantize(TWOPLACES)