from sqlalchemy.orm.session import Session

from db.models import DbNSFW
from ML.nsfw import MLHandler


def populate(db: Session, blog_id: int, ml_info: MLHandler):
    new_nsfw = DbNSFW(
        blog_id=blog_id,
        nsfw_prob=ml_info.prob,
        nsfw_flag=ml_info.nsfw,
        model_name=ml_info.model_name,
        model_type=ml_info.model_type
    )
    db.add(new_nsfw)
    db.commit()
    db.refresh(new_nsfw)
    return new_nsfw
