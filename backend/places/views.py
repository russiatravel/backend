from flask import Blueprint, request

from backend.errors import AppError
from backend.photos.schemas import Photo
from backend.photos.storages import OnlineStorage as PhotoStorage
from backend.places.schemas import Place
from backend.places.storages import OnlineStorage

place_view = Blueprint('places', __name__)

storage = OnlineStorage()
photo_storage = PhotoStorage()


@place_view.post('/')
def add():
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1

    place = Place(**payload)

    place = storage.add(place)
    return place.dict(), 201


"""@place_view.get('/')
def get_all():
    places = storage.get_all()
    return [place.dict() for place in places], 200"""


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


@place_view.get('/<int:uid>/photos/')
def get_photos(uid):
    photos = photo_storage.get_for_place(uid)

    return [photo.dict() for photo in photos], 200


@place_view.post('/<int:uid>/photos/')
def add_photo(uid):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    payload['place_id'] = uid

    photo = Photo(**payload)

    photo = photo_storage.add(photo)
    return photo.dict(), 201


@place_view.delete('/<int:uid>/photos/<int:photo_uid>')
def delete_photo(uid, photo_uid):
    photo_storage.delete(uid, photo_uid)

    return {}, 204


@place_view.get('/')
def get_place(name=''):
    if 'name' in request.args:
        name = request.args.get('name')
        return storage.get_by_name(name).dict()

    places = storage.get_all()
    return [place.dict() for place in places], 200
