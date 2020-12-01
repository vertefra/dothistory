import json
import datetime

from project.app.schemas import articles


def test_create_article(test_app_with_db):

    payload = articles.AuthorRequestPayload(
        title="New article Title",
        content="""Lorem Ipsum is simply dummy text of the
        printing and typesetting industry. Lorem Ipsum has been
        the industry's standard dummy text ever since the 1500s,
        when an unknown printer took a galley of type and scrambled
        it to make a type specimen book. It has survived not only
        five centuries, but also the leap into electronic typesetting,
        remaining essentially unchanged. It was popularised in the 1960s
        with the release of Letraset sheets containing Lorem Ipsum
        passages, and more recently with desktop publishing software
        like Aldus PageMaker including versions of Lorem Ipsum."""
        category="category 1"
        sub_category="sub category 1"
        date=datatime.datetime(2020, 11, 30)
        period_from=datetime.datetime(1987, 2, 9)
        period_to=datetime.datetime(2000, 2, 9)
