
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from project.app.database.db import db_engine
from project.app.schemas.authors import AuthorRequestPayload, Author
from project.app.schemas.authors import AuthorResponsePayload

router = APIRouter()


# desc: add a author to the database
# route: POST - /authors/
# private

@router.post(
    "/",
    response_model=AuthorResponsePayload,
    status_code=201
)
async def create_author(
        author_payload: AuthorRequestPayload,
        db: Session = Depends(db_engine.get_db)
):
    try:
        created_author = Author.create_author(
            author_payload, db, password=author_payload.password)
        return created_author

    except IntegrityError:
        raise HTTPException(status_code=400, detail={
            "success": False, "error": "duplicate key"})


# desc: retrieve all the authors from database
# route: GET - /authors/
# private

@router.get(
    "/",
    responses={404: {"model": str}, 200: {"model": list}},
    status_code=200
)
async def find_all_authors(
    db: Session = Depends(db_engine.get_db)
):
    try:
        all_authors = Author.get_all_authors(db)
        if len(all_authors) > 0:
            return all_authors
        return JSONResponse(
            status_code=404, content={"error": "items not found"})

    except IntegrityError:
        raise HTTPException(status_code=500, detail={
            "sucess": False, "error": "Cannot retrieve authors"})


# desc:     get author from database by its id
# route:    GET - /authors/{id}
# public

@router.get(
    "/{id}",
    status_code=200,
    response_model=AuthorResponsePayload
)
async def find_author_by_id(
    id: int,
    db: Session = Depends(db_engine.get_db)
):
    '''
    desc:   get author from database by its id
    route:  GET - /authors/{id}
    public
    '''

    author = Author.get_author_by_id(db, id)

    if author is not None:
        return author
    else:
        raise HTTPException(status_code=404, detail="Author not found")


# desc:     update author
# route:    PUT - /authors/{id}
# private

@router.put(
    "/{id}",
    status_code=203,
    response_model=AuthorResponsePayload
)
async def update_author(
    id: int,
    updated_author_payload: AuthorRequestPayload,
    db: Session = Depends(db_engine.get_db)
):
    '''
    desc:   update author
    route:  PUT - /authors/{id}
    private
    '''
    try:
        updated_author = Author.update_author(db, id, updated_author_payload)
        return updated_author
    except IntegrityError as err:
        print(err)
