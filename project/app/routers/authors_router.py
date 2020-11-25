
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from project.app.database.db import db_engine
from project.app.schemas.authors import AuthorRequestPayload, Author
from project.app.schemas.authors import AuthorResponsePayload

router = APIRouter()


@router.post("/", response_model=AuthorResponsePayload, status_code=201)
async def create_author(
        author_payload: AuthorRequestPayload,
        db: Session = Depends(db_engine.get_db)):
    try:
        created_author = Author.create_author(
            author_payload, db, password=author_payload.password)
        return created_author

    except IntegrityError:
        raise HTTPException(status_code=400, detail={
                            "success": False, "error": "duplicate key"})
