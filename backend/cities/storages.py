from backend.cities.schemas import City as CitySchema
from backend.database import db_session
from backend.errors import NotFoundError
from backend.models import City


class OnlineStorage():
    def add(self, city: CitySchema) -> CitySchema:
        entity = City(name=city.name, description=city.description)

        db_session.add(entity)
        db_session.commit()

        return CitySchema(uid=entity.uid, name=entity.name, description=entity.description)

    def update(self, uid: int, city: CitySchema) -> CitySchema:
        entity = City.query.get(uid)

        if not entity:
            raise NotFoundError('cities', uid)

        entity.name = city.name
        entity.description = city.description

        db_session.commit()

        return CitySchema(uid=entity.uid, name=entity.name, description=entity.description)

    def delete(self, uid: int) -> None:
        entity = City.query.get(uid)

        if not entity:
            raise NotFoundError('cities', uid)

        db_session.delete(entity)
        db_session.commit()

    def get_by_id(self, uid: int) -> CitySchema:
        entity = City.query.get(uid)

        if not entity:
            raise NotFoundError('cities', uid)

        return CitySchema(uid=entity.uid, name=entity.name, description=entity.description)

    def get_all(self) -> list[CitySchema]:
        entity = City.query.all()
        all_cities = []

        for city in entity:
            poi = CitySchema(uid=city.uid, name=city.name, description=city.description)
            all_cities.append(poi)

        return all_cities

    def get_by_name(self, name: str) -> list[CitySchema]:
        entities = City.query.filter(City.name.ilike(name)).all()

        if not entities:
            raise NotFoundError(name, 0)

        all_cities = []

        for entity in entities:
            city = CitySchema(uid=entity.uid, name=entity.name, description=entity.description)
            all_cities.append(city)

        return all_cities
