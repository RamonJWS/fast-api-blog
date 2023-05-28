from sqlalchemy.orm.session import Session

from schemas import BlogPost


def populate(db: Session, request: BlogPost):
    pass
