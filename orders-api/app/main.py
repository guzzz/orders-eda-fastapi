from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.models import user, order
from app.config.database import SessionLocal, engine
from app.controllers import user_controller
from app.controllers import order_controller
from app.errors import CustomError


user.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(
    user_controller.router,
    prefix="/v0/users",
    tags=["Users"]
)
app.include_router(
    order_controller.router,
    prefix="/v0/orders",
    tags=["Orders"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return CustomError.get_error(exc)

@app.exception_handler(IntegrityError)
async def validation_exception_handler(request, exc):
    return CustomError.get_integrity_error(exc)
