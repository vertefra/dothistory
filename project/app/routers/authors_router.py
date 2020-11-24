from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from project.app.database.db import get_db
from project.app.schemas.authors import AuthorRequestPayload, Author
from project.app.schemas.authors import AuthorResponsePayload

router = APIRouter()


@router.post("/", response_model=AuthorResponsePayload)
async def create_author(
        author_payload: AuthorRequestPayload,
        db: Session = Depends(get_db)):

    created_author = Author.create_author(
        author_payload, db, password=author_payload.password)

    return created_author
