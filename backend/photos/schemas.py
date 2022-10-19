from pydantic import BaseModel


class Photo(BaseModel):
    uid: int
    place_id: int
    image_url: str
