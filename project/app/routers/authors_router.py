from project.app.database.db import get_db, engine
from fastapi import APIRouter

from project.app.schemas.authors import AuthorRequestPayload, Author
from project.app.schemas.authors import AuthorResponsePayload

router = APIRouter()


@router.post("/", response_model=AuthorResponsePayload)
def create_author(author_payload: AuthorRequestPayload):

    db = get_db(engine)
    created_author = Author.create_author(
        author_payload, db, password=author_payload.password)

    return created_author
