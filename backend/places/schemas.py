from pydantic import BaseModel


class Place(BaseModel):
    uid: int
    name: str
    description: str
    city_id: int
    preview_image_url: str
