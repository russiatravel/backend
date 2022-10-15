from backend.database import db_session
from backend.errors import NotFoundError
from backend.models import Place
from backend.places.schemas import Place as PlaceSchema


class OnlineStorage():
    def add(self, place: PlaceSchema) -> PlaceSchema:
        entity = Place(name=place.name, description=place.description)

        db_session.add(entity)
        db_session.commit()

        return PlaceSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def update(self, uid: int, place: PlaceSchema) -> PlaceSchema:
        entity = Place.query.get(uid)

        if not entity:
            raise NotFoundError('places', uid)

        entity.name = place.name
        entity.description = place.description

        db_session.commit()

        return PlaceSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def delete(self, uid: int) -> None:
        entity = Place.query.get(uid)

        if not entity:
            raise NotFoundError('places', uid)

        db_session.delete(entity)
        db_session.commit()

    def get_by_id(self, uid: int) -> PlaceSchema:
        entity = Place.query.get(uid)

        if not entity:
            raise NotFoundError('places', uid)

        return PlaceSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def get_all(self) -> list[PlaceSchema]:
        entity = Place.query.all()
        all_places = []

        for place in entity:
            poi = PlaceSchema(uid=place.uid, name=place.name, description=place.description)
            all_places.append(poi)

        return all_places
