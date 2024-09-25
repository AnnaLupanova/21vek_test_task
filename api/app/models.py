from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    text = Column(String(256))
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='posts')


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(56))
    second_name = Column(String(56))
    posts = relationship('Post', back_populates='author')
