import datetime

from pydantic import BaseModel


class CreateOrder(BaseModel):
    customer_id: int
    delivery_date: datetime.date


class UpdateOrder(BaseModel):
    id: int
    customer_id: int
    status: str
    delivery_date: datetime.date

