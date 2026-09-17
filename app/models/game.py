from sqlalchemy import Column, Integer, String, Float, Text, BigInteger

from app.core.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    igdb_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String, nullable=False)
    release_date = Column(BigInteger, nullable=True)
    rating = Column(Float, nullable=True)
    genres = Column(String, nullable=True)
    cover_image_id = Column(String, nullable=True)
    summary = Column(Text, nullable=True)