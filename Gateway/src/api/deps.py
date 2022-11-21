from sqlmodel import Session

from src.db.session import engine


def get_session():
    with Session(engine) as session:
        yield session
