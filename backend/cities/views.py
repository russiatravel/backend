from flask import Blueprint, request

from backend.errors import AppError
from backend.cities.schemas import City
from backend.cities.storages import OnlineStorage

city_view = Blueprint('cities', __name__)

storage = OnlineStorage()


@city_view.post('/')
def add():
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1

    city = City(**payload)

    city = storage.add(city)
    return city.dict(), 201


@city_view.get('/')
def get_all():
    cities = storage.get_all()
    return [city.dict() for city in cities], 200


@city_view.get('/<int:uid>')
def get_by_id(uid):
    city = storage.get_by_id(uid)

    return city.dict(), 200


@city_view.put('/<int:uid>')
def update_by_id(uid):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = uid
    city = City(**payload)
    city = storage.update(uid, city)

    return city.dict(), 200


@city_view.delete('/<int:uid>')
def delete_city(uid):
    storage.delete(uid)

    return {}, 204
