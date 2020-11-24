from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError

from project.app.models import authors


class Author(BaseModel):
    name: str
    email: str
    bio: Optional[str]
    profile_pic: Optional[str]
    articles: Optional[List] = []

    class Config:
        orm_mode = True

    def create_author(self, db: Session, password):
        self.password = password

        new_author = authors.Author(**self.dict())

        db.add(new_author)
        db.commit()
        db.refresh(new_author)

        return new_author

    def __repr__(self):
        return {
            "name": self.name,
            "email": self.email
        }


class AuthorResponsePayload(Author):
    id: int


class AuthorRequestPayload(Author):
    password: str
