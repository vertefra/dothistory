from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from project.app.database.db import db_engine

Base = db_engine.base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    bio = Column(Text)
    profile_pic = Column(String)

    # backpopulate the "author" field in the articles table

    articles = relationship("Article", back_populates=("author"))
