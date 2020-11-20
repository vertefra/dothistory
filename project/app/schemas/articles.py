from pydantic import BaseModel

import datetime


class ArticleBaseSchema(BaseModel):
    title: str
    content: str
    main_pic: str
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


class ArticleResponsePayload(ArticleBaseSchema):
    id: int


class AuthorRequestPayload(ArticleBaseSchema):
    id: int
