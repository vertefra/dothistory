from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship

from project.app.database.db import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    main_pic = Column(String)

    # Articles identifier

    category = Column(String)
    sub_category = Column(String)

    date = Column(Date)
    period_from = Column(Date)
    period_to = Column(Date)

    event_tag = Column(String)
    concept_tag = Column(String)
    party_tag = Column(String)
    people_tag = Column(String)

    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("Author")
