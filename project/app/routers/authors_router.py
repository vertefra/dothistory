from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError

from project.app.database.db import db_engine
from project.app.schemas.authors import AuthorRequestPayload, Author
from project.app.schemas.authors import AuthorResponsePayload

router = APIRouter()


@router.post("/", response_model=AuthorResponsePayload, status_code=201)
async def create_author(
        author_payload: AuthorRequestPayload,
        db: Session = Depends(db_engine.get_db)):
    print('--------- processing request --------------')
    try:
        print("--------------try block---------------------")
        created_author = Author.create_author(
            author_payload, db, password=author_payload.password)
        print("------------endblock -------------------")
        return created_author

    except Exception as err:
        raise HTTPException(status_code=404, detail=err)
        return
