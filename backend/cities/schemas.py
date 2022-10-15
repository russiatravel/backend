from pydantic import BaseModel


class City(BaseModel):
    uid: int
    name: str
    description: str
