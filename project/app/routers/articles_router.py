from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from project.app.database.db import db_engine
from project.app.schemas.articles import ArticleResponsePayload, Article
from project.app.schemas.articles import ArticleRequestPayload

router = APIRouter()


# desc: add an article to the database
# route: POST - /articles/
# private

@router.post(
    "/",
    response_model=ArticleResponsePayload,
    status_code=201
)
async def create_author(
        article_payload: ArticleRequestPayload,
        db: Session = Depends(db_engine.get_db)
):
    '''
    desc: Add an article to the database with
    author_id referencing an author entry
    route: POST - /articles/
    private
    '''

    try:
        created_article = Article.create_article(
            article_payload, db
        )

        return created_article

    except IntegrityError:
        raise HTTPException(status_code=400, detail={
            "success": False, "error": "duplicate title"})
