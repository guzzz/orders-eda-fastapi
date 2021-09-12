import uuid
from sqlalchemy.orm import Session
from structlog import get_logger

from app.models.user import User
from app.schemas import user_schema as schema
from app.utils.dates import now

log = get_logger()


class UserRepository:

    def __init__(self):
        pass

    def retrieve(self, db: Session, id: str):
        return db.query(User).filter(User.id == id).first()

    def list(self, db: Session, page, limit):
        log.info(f"[DB] Listing USER page {page}, page_size: {limit}.")
        to_start = (page-1)*limit
        return db.query(User).offset(to_start).limit(limit).all()

    def create(self, db: Session, user: dict):
        log.info("[DB] Creating USER.")
        db_user = User(
            id=uuid.uuid4(),
            name=user.get("name"),
            cpf=user.get("cpf"),
            email=user.get("email"),
            phone_number=user.get("phone_number"),
            created_at=now(),
            updated_at=now()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, id: str, user: dict):
        log.info(f"[DB] Updating USER {id}")
        user_db = db.query(User).filter(User.id == id).first()
        if user_db:
            db.query(User).filter(User.id == id).update(
                {
                    "name": user.get("name"),
                    "cpf": user.get("cpf"),
                    "email": user.get("email"),
                    "phone_number": user.get("phone_number"),
                    "updated_at": now()
                }, 
            synchronize_session="fetch")
            db.commit()
            return user_db
        else:
            return False

    def delete(self, db: Session, id: str):
        log.info(f"[DB] Deleting USER {id}")
        user_db = db.query(User).filter(User.id == id).first()
        if user_db:
            db.query(User).filter(User.id == id).delete(synchronize_session="fetch")
            db.commit()
            return True
        else:
            return False

    def eda_create(self, db: Session, user: dict):
        log.info("[EDA DB] Creating USER.")
        db_user = User(
            id=user.get("id"),
            name=user.get("name"),
            cpf=user.get("cpf"),
            email=user.get("email"),
            phone_number=user.get("phone_number"),
            created_at=user.get("created_at"),
            updated_at=user.get("updated_at")
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    def eda_update(self, db: Session, id: str, user: dict):
        log.info(f"[EDA DB] Updating USER {id}")
        db.query(User).filter(User.id == id).update(
                {
                    "name": user.get("name"),
                    "cpf": user.get("cpf"),
                    "email": user.get("email"),
                    "phone_number": user.get("phone_number"),
                    "updated_at": user.get("updated_at")
                }, 
            synchronize_session="fetch")
        db.commit()
        
    def eda_delete(self, db: Session, id: str):
        log.info(f"[EDA DB] Deleting USER {id}")
        db.query(User).filter(User.id == id).delete(synchronize_session="fetch")
        db.commit()
