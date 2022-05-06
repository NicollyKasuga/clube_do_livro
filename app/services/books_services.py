from app.exc.type_exc import TypeValueError
from app.models import Genre, Author

from sqlalchemy.orm import Session
from typing import Union


def define_authors_or_genres(
    authors_or_genres: list[str],
    session: Session,
    Model: Union[Genre, Author],
):
    response = []
    for author_or_genre_name in authors_or_genres:
        author_or_genre_name = author_or_genre_name.lower()
        found_author_or_genre = (
            session.query(Model).filter_by(name=author_or_genre_name).first()
        )

        if not found_author_or_genre:
            try:
                author_or_genre = Model(name=author_or_genre_name)
            except TypeValueError as e:
                return e.message, e.status_code

            session.add(author_or_genre)
            response.append(author_or_genre)
            session.commit()

        else:
            response.append(found_author_or_genre)

    return response
