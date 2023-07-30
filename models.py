from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = 'postgresql://postgres:admin123@postgresql:5432/MovieReviewsSentiments'
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movie_table'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    original_language = Column(String, nullable=False)
    reviews = relationship('Review', back_populates='movie', cascade='all, delete-orphan')


class Review(Base):
    __tablename__ = 'review_table'
    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    review = Column(String, nullable=False)
    movie_id = Column(Integer, ForeignKey('movie_table.id'))
    movie = relationship('Movie', back_populates='reviews')


Base.metadata.create_all(engine)
