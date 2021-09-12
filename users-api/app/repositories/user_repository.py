from pymongo.errors import InvalidId
from structlog import get_logger

from app.config.db import mongoclient

log = get_logger()


class UserRepository:

    def __init__(self):
        database = mongoclient.local
        self._users = database.user

    def retrieve(self, id, uuid=True):
        try:
            log.info("[DB] Searching USER...")
            if uuid:
                return self._users.find_one({"id": id})
            else:
                return self._users.find_one({"_id": id})
        except InvalidId:
            log.info("[DB] Invalid ID")
            return False

    def list(self, page, limit):
        log.info(f"[DB] Listing USER page {page}, page_size: {limit}.")
        to_start = (page-1)*limit
        return self._users.find().skip(to_start).limit(limit)

    def create(self, user):
        log.info("[DB] Creating USER...")
        return self._users.insert_one(user)

    def update(self, uuid, user):
        try:
            log.info(f"[DB] Updating USER: {uuid}")
            result = self._users.find_one_and_update(
                {"id": uuid}, {"$set": user}
            )
            return result
        except InvalidId:
            log.info("[DB] Invalid ID")
            return False

    def delete(self, uuid):
        try:
            log.info(f"[DB] Deleting USER: {uuid}")
            return self._users.find_one_and_delete({"id": uuid})
        except InvalidId:
            log.info("[DB] Invalid ID")
            return False