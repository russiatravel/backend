from backend.places.database import Base, engine
from sqlalchemy import Column, Integer, String


class Poi(Base):
    __tablename__ = 'places'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
