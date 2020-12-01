from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from project.app.models import articles

import datetime


class Article(BaseModel):
    title: str = "Article Title"
    content: str = "Aritcle Content"
    main_pic: str = "pic link"
    category: str
    sub_category: str
    date: datetime
    period_from: datetime
    period_to: datetime
    event_tag: str
    concept_tag: str
    party_tag: str
    people: str
    author_id: int

    class Config:
        orm_mode = True

    def create_article(self, db: Session):
        ''' Creates a new article associated with author_id '''

        new_article = articles.Article(**self.dict())

        try:
            db.add(new_article)
            db.commit()
            db.refresh(new_article)
            return new_article

        except IntegrityError as err:
            db.rollback()
            raise err


class ArticleResponsePayload(Article):
    id: int


class AuthorRequestPayload(Article):
    id: int
