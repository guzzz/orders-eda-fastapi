from typing import Optional
from uuid import UUID
from typing import List

from fastapi import APIRouter, status, Response, Depends, Header
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.services.order_service import OrderService
from app.config.database import get_db
from app.schemas import order_schema as schema

router = InferringRouter()
order_service = OrderService()


@cbv(router)
class OrderController:

    @router.get("/", response_model=List[schema.OrderList])
    def find_all_orders(
        self, db: Session = Depends(get_db), page: Optional[int] = Header(1), 
        limit: Optional[int] = Header(10), user_id: Optional[UUID] = None
    ):
        return order_service.list(db, page, limit, user_id)

    @router.get("/{uuid}", status_code=200, response_model=schema.OrderInfo)
    def find_one_order(self, uuid: UUID, response: Response, db: Session = Depends(get_db)):
        search_result = order_service.retrieve(db, uuid)
        if search_result:
            return search_result
        else:
            message = {"message": f"It was not possible to find the order_id: {uuid}"}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=message
            )

    @router.post("/", status_code=201, response_model=schema.OrderInfo)
    def create_order(self, order: schema.Order, db: Session = Depends(get_db)):
        return order_service.create(db, order)

    @router.delete("/{uuid}", status_code=204)
    def delete_order(self, uuid: UUID, response: Response, db: Session = Depends(get_db)):
        deleted = order_service.delete(db, uuid)
        if deleted:
            return
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"It was not possible to find and delete the id: {uuid}"}


    @router.put("/{uuid}", status_code=200, response_model=schema.OrderInfo)
    def update_order(self, uuid: UUID, order: schema.Order, db: Session = Depends(get_db)):
        result = order_service.update(db, uuid, order)
        if result:
            return result
        else:
            message = {"message": f"It was not possible to find the order_id: {uuid}"}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=message
            )
