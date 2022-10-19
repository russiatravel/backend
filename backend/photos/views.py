from flask import Blueprint, request

from backend.errors import AppError
from backend.photos.schemas import Photo
from backend.photos.storages import OnlineStorage

photo_view = Blueprint('photos', __name__)

storage = OnlineStorage()


@photo_view.post('/')
def add():
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1

    photo = Photo(**payload)

    photo = storage.add(photo)
    return photo.dict(), 201


@photo_view.delete('/<int:uid>')
def delete_photo(uid):
    storage.delete(uid)

    return {}, 204
