
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

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


@router.get("/",
            responses={404: {"model": str}, 200: {"model": list}},
            status_code=200)
async def find_all_authors(db: Session = Depends(db_engine.get_db)):
    try:
        all_authors = Author.get_all_authors(db)
        if len(all_authors) > 0:
            return all_authors
        return JSONResponse(
            status_code=404, content={"error": "items not found"})

    except IntegrityError:
        raise HTTPException(status_code=500, detail={
            "sucesso": False, "error": "Cannot retrieve authors"})
