from pydantic import BaseModel
from typing import List


class AuthorBaseSchema(BaseModel):
    name: str
    email: str
    bio: str
    profile_pic: str
    articles: List


class AuthorResponsePayload(AuthorBaseSchema):
    id: int


class AuthorRequestPayload(AuthorBaseSchema):
    password: str
