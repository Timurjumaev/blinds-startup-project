from pydantic import BaseModel


class CreatePhone(BaseModel):
    number: str
    comment: str

