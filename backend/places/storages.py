from backend.errors import NotFoundError
from backend.database import db_session
from backend.models import Place
from backend.places.schemas import Place as PlaceSchema


class LocalStorage:
    def __init__(self):
        self.places: dict[int, PlaceSchema] = {}
        self.last_uid = 0

    def add(self, place: PlaceSchema) -> PlaceSchema:
        self.last_uid += 1
        place.uid = self.last_uid
        self.places[self.last_uid] = place
        return place

    def get_all(self) -> list[PlaceSchema]:
        return list(self.places.values())

    def get_by_id(self, uid: int) -> PlaceSchema:
        if uid not in self.places:
            raise NotFoundError('places', uid)

        return self.places[uid]

    def update(self, uid: int, place: PlaceSchema) -> PlaceSchema:
        if uid not in self.places:
            raise NotFoundError('places', uid)

        self.places[uid] = place
        return place

    def delete(self, uid: int) -> None:
        if uid not in self.places:
            raise NotFoundError('places', uid)

        self.places.pop(uid)


class OnlineStorage(LocalStorage):
    def add(self, place: PlaceSchema) -> PlaceSchema:
        entity = Place(name=place.name, description=place.description)

        db_session.add(entity)
        db_session.commit()

        return PlaceSchema(uid=entity.uid, name=entity.name, description=entity.description)
