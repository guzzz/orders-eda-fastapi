import uuid
from sqlalchemy.orm import Session
from structlog import get_logger

from app.models.order import Order
from app.schemas import order_schema as schema
from app.utils.dates import now

log = get_logger()


class OrderRepository:

    def __init__(self):
        pass

    def retrieve(self, db: Session, id: str):
        log.info("[DB] Searching ORDER...")
        return db.query(Order).filter(Order.id == id).first()

    def list(self, db: Session, page, limit, user_id_filter):
        log.info(f"[DB] Listing ORDER page {page}, page_size: {limit}.")
        to_start = (page-1)*limit
        if user_id_filter:
            user = str(user_id_filter)
            return db.query(Order).filter(Order.user_id == user).offset(to_start).limit(limit).all()
        else:
            return db.query(Order).offset(to_start).limit(limit).all()

    def create(self, db: Session, order: dict):
        log.info("[DB] Creating ORDER...")
        db_order = Order(
            id=uuid.uuid4(),
            item_description=order.get("item_description"),
            item_quantity=order.get("item_quantity"),
            item_price=order.get("item_price"),
            total_value=order.get("total_value"),
            user_id=order.get("user_id"),
            created_at=now(),
            updated_at=now()
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    def update(self, db: Session, id: str, order: dict):
        order_db = db.query(Order).filter(Order.id == id).first()
        if order_db:
            log.info(f"[DB] Updating ORDER: {id}")
            db.query(Order).filter(Order.id == id).update(
                {
                    "id": order_db.id,
                    "item_description": order.get("item_description"),
                    "item_quantity": order.get("item_quantity"),
                    "item_price": order.get("item_price"),
                    "total_value": order.get("total_value"),
                    "user_id": order.get("user_id"),
                    "created_at": order_db.created_at,
                    "updated_at": now()
                }, 
            synchronize_session="fetch")
            db.commit()
            return order_db
        else:
            log.info(f"[DB] ID {id} Not found")
            return False

    def delete(self, db: Session, id: str):
        order_db = db.query(Order).filter(Order.id == id).first()
        if order_db:
            log.info(f"[DB] Deleting ORDER: {id}")
            db.query(Order).filter(Order.id == id).delete(synchronize_session="fetch")
            db.commit()
            return True
        else:
            log.info(f"[DB] ID {id} Not found")
            return False
        