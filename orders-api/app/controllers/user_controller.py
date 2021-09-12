from typing import Optional
from uuid import UUID
from typing import List

from fastapi import APIRouter, status, Response, Depends, Header
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.config.database import get_db
from app.schemas import user_schema as schema
from app.producer import publish

router = InferringRouter()
user_service = UserService()


@cbv(router)
class UserController:

    @router.get("/", response_model=List[schema.UserInfo])
    def find_all_users(self, db: Session = Depends(get_db), page: Optional[int] = Header(1), limit: Optional[int] = Header(10)):
        return user_service.list(db, page, limit)

    @router.get("/{uuid}", status_code=200, response_model=schema.UserInfo)
    def find_one_user(self, uuid: UUID, response: Response, db: Session = Depends(get_db)):
        search_result = user_service.retrieve(db, uuid)
        if search_result:
            return search_result
        else:
            message = {"message": f"It was not possible to find the user_id: {uuid}"}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=message
            )

    @router.post("/", status_code=201, response_model=schema.UserInfo, include_in_schema=False)
    def create_user(self, user: schema.User, db: Session = Depends(get_db)):
        publish("teste0", "teste1")
        return user_service.create(db, user)

    @router.delete("/{uuid}", status_code=204, include_in_schema=False)
    def delete_user(self, uuid: UUID, response: Response, db: Session = Depends(get_db)):
        deleted = user_service.delete(db, uuid)
        if deleted:
            return
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"It was not possible to find and delete the id: {uuid}"}


    @router.put("/{uuid}", status_code=200, response_model=schema.UserInfo, include_in_schema=False)
    def update_user(self, uuid: UUID, user: schema.User, db: Session = Depends(get_db)):
        result = user_service.update(db, uuid, user)
        if result:
            return result
        else:
            message = {"message": f"It was not possible to find the user_id: {uuid}"}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=message
            )
