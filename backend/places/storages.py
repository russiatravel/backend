from sqlalchemy.exc import IntegrityError

from backend.database import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import City, Place
from backend.places.schemas import Place as PlaceSchema


class OnlineStorage():
    name = 'places'

    def add(self, place: PlaceSchema) -> PlaceSchema:
        entity = Place(
            name=place.name,
            description=place.description,
            city_id=place.city_id,
            preview_image_url=place.preview_image_url,
        )

        try:
            db_session.add(entity)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return PlaceSchema(
            uid=entity.uid,
            name=entity.name,
            description=entity.description,
            city_id=entity.city_id,
            preview_image_url=entity.preview_image_url,
        )

    def update(self, uid: int, place: PlaceSchema) -> PlaceSchema:
        entity = Place.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        entity.name = place.name
        entity.description = place.description

        db_session.commit()

        return PlaceSchema(
            uid=entity.uid,
            name=entity.name,
            description=entity.description,
            city_id=entity.city_id,
            preview_image_url=entity.preview_image_url,
        )

    def delete(self, uid: int) -> None:
        entity = Place.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        db_session.delete(entity)
        db_session.commit()

    def get_by_id(self, uid: int) -> PlaceSchema:
        entity = Place.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        return PlaceSchema(
            uid=entity.uid,
            name=entity.name,
            description=entity.description,
            city_id=entity.city_id,
            preview_image_url=entity.preview_image_url,
        )

    def get_all(self) -> list[PlaceSchema]:
        entities = Place.query.all()
        all_places = []

        for place in entities:
            poi = PlaceSchema(
                uid=place.uid,
                name=place.name,
                description=place.description,
                city_id=place.city_id,
                preview_image_url=place.preview_image_url,
            )

            all_places.append(poi)

        return all_places

    def get_for_city(self, uid: int) -> list[PlaceSchema]:
        city = City.query.get(uid)

        if not city:
            raise NotFoundError('cities', uid)

        entities = city.places

        all_places = []

        for place in entities:
            poi = PlaceSchema(
                uid=place.uid,
                name=place.name,
                description=place.description,
                city_id=place.city_id,
                preview_image_url=place.preview_image_url,
            )

            all_places.append(poi)

        return all_places

    def find_for_city(self, uid: int, name: str) -> list[PlaceSchema]:
        search = '%{}%'.format(name)
        entities = Place.query.filter(
            Place.city_id == uid,
            Place.name.ilike(search),
        ).all()

        target_places = []

        if not entities:
            raise NotFoundError(name, uid)

        for entity in entities:
            place = PlaceSchema(
                uid=entity.uid,
                name=entity.name,
                description=entity.description,
                city_id=entity.city_id,
                preview_image_url=entity.preview_image_url,
            )

            target_places.append(place)

        return target_places
