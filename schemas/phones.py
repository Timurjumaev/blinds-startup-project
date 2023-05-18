from pydantic import BaseModel


class CreatePhone(BaseModel):
    number: str
    comment: str



class UpdatePhone(BaseModel):
    id: int
    number: str
    comment: str

