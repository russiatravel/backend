from flask import Blueprint, request

from backend.errors import AppError
from backend.places.schemas import Place
from backend.places.storages import LocalStorage, OnlineStorage

place_view = Blueprint('places', __name__)

storage = LocalStorage()
storage2 = OnlineStorage()


@place_view.post('/')
def add():
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1

    place = Place(**payload)

    place = storage2.add(place)
    return place.dict(), 201


@place_view.get('/')
def get_all():
    places = storage.get_all()
    return [place.dict() for place in places], 200


@place_view.get('/<int:uid>')
def get_by_id(uid):
    place = storage.get_by_id(uid)

    return place.dict(), 200


@place_view.put('/<int:uid>')
def update_by_id(uid):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = uid
    place = Place(**payload)
    place = storage.update(uid, place)

    return place.dict(), 200


@place_view.delete('/<int:uid>')
def delete_place(uid):
    storage.delete(uid)

    return {}, 204
