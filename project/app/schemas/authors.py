from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError


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
        try:
            db.add(**self.dict())
            db.commit()
            db.refresh(self)
            return self
        except InvalidRequestError as err:
            db.rollback()
            print("ERROR while trying to create new Author: ", err)

    def __repr__(self):
        return {
            "name": self.name,
            "email": self.email
        }


class AuthorResponsePayload(Author):
    id: int


class AuthorRequestPayload(Author):
    password: str
