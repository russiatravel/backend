from backend.errors import NotFoundError
from backend.places.schemas import Place


class LocalStorage:
    def __init__(self):
        self.places: dict[int, Place] = {}
        self.last_uid = 0

    def add(self, place: Place) -> Place:
        self.last_uid += 1
        place.uid = self.last_uid
        self.places[self.last_uid] = place
        return place

    def get_all(self) -> list[Place]:
        return list(self.places.values())

    def get_by_id(self, uid: int) -> Place:
        if uid not in self.places:
            raise NotFoundError('places', uid)

        return self.places[uid]

    def update(self, uid: int, place: Place) -> Place:
        if uid not in self.places:
            raise NotFoundError('places', uid)

        self.places[uid] = place
        return place

    def delete(self, uid: int) -> None:
        if uid not in self.places:
            raise NotFoundError('places', uid)

        self.places.pop(uid)
