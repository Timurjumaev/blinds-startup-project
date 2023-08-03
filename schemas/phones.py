from pydantic import BaseModel


class CreatePhone(BaseModel):
    number: int
    comment: str

