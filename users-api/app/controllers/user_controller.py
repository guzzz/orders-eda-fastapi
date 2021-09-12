from typing import Optional
from uuid import UUID

from fastapi_utils.cbv import cbv
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, status, Response, Header
from fastapi_utils.inferring_router import InferringRouter

from app.models.user import User
from app.services.user_service import UserService

router = InferringRouter()
user_service = UserService()


@cbv(router)
class UserController:

    @router.get("/")
    def find_all_users(self, page: Optional[int] = Header(1), limit: Optional[int] = Header(10)):
        return user_service.list(page, limit)

    @router.get("/{uuid}", status_code=200)
    def find_one_user(self, uuid: UUID, response: Response):
        search_result = user_service.retrieve(uuid)
        if search_result:
            return search_result
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"It was not possible to find the user_id: {uuid}"}

    @router.post("/", status_code=201)
    def create_user(self, user: User):
        user = user_service.create(user)
        return user

    @router.put("/{uuid}", status_code=200)
    def update_user(self, uuid: UUID, user: User, response: Response):
        updated_info = user_service.update(uuid, user)
        if updated_info:
            return updated_info
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"It was not possible to update the user_id: {uuid}"}

    @router.delete("/{uuid}", status_code=204)
    def delete_user(self, uuid: UUID, response: Response):
        deleted = user_service.delete(uuid)
        if deleted:
            return
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"It was not possible to find and delete the id: {uuid}"}
