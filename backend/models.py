from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base, engine


class Place(Base):
    __tablename__ = 'places'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    city_id = Column(Integer, ForeignKey('cities.uid'), nullable=False)
    preview_image_url = Column(String)

    photos = relationship('Photo')


class City(Base):
    __tablename__ = 'cities'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    places = relationship('Place')


class Photo(Base):
    __tablename__ = 'photos'

    uid = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.uid'), nullable=False)
    image_url = Column(String)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
