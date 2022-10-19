from sqlalchemy.exc import IntegrityError

from backend.database import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Photo, Place
from backend.photos.schemas import Photo as PhotoSchema


class OnlineStorage():
    name = 'photos'

    def add(self, photo: PhotoSchema) -> PhotoSchema:
        entity = Photo(
            place_id=photo.place_id,
            image_url=photo.image_url,
        )

        try:
            db_session.add(entity)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return PhotoSchema(
            uid=entity.uid,
            place_id=entity.place_id,
            image_url=entity.image_url,
        )

    def delete(self, uid: int) -> None:
        entity = Photo.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        db_session.delete(entity)
        db_session.commit()

    def get_for_place(self, uid: int) -> list[PhotoSchema]:
        place = Place.query.get(uid)

        if not place:
            raise NotFoundError('places', uid)

        entities = place.photos

        all_photos = []

        for entity in entities:
            photo = PhotoSchema(
                uid=entity.uid,
                place_id=entity.place_id,
                image_url=entity.image_url,
            )

            all_photos.append(photo)

        return all_photos
