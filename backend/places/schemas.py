from pydantic import BaseModel


class Place(BaseModel):
    uid: int
    name: str
    description: str | None
    city_id: int
    preview_image_url: str | None
