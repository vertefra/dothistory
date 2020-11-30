from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from project.app.models import authors


class Author(BaseModel):
    name: str
    email: str
    bio: Optional[str]
    profile_pic: Optional[str]
    articles: Optional[List] = []

    class Config:
        orm_mode = True

    def create_author(self, db: Session, password: str):
        self.password = password

        new_author = authors.Author(**self.dict())

        try:
            db.add(new_author)
            db.commit()
            db.refresh(new_author)
            return new_author

        except IntegrityError as err:
            db.rollback()
            raise err

    def get_all_authors(db: Session):
        ''' returns all the authors in the database without password column '''

        all_authors = []

        try:
            all_authors = db.query(authors.Author).all()
            sanitized_authors = []

            for author in all_authors:
                author.password = None
                sanitized_authors.append(author)

            return sanitized_authors

        except IntegrityError as err:
            raise err

    def get_author_by_id(db: Session, id: int):
        ''' returns and author filtered by its ID '''

        found_author = db.query(authors.Author).filter_by(
            id=id).one_or_none()

        print("found:", found_author)

        return found_author

    def __repr__(self):
        return {
            "name": self.name,
            "email": self.email
        }


class AuthorResponsePayload(Author):
    id: int


class AuthorRequestPayload(Author):
    password: str
