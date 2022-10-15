from sqlalchemy import Column, Integer, String

from backend.database import Base, engine


class Place(Base):
    __tablename__ = 'places'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class City(Base):
    __tablename__ = 'cities'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
