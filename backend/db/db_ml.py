from sqlalchemy.orm.session import Session

from db.models import DbNSFW


def populate(db: Session, blog_id: int, probability: float, nsfw_flag: bool, model_name: str, model_type: str):
    new_nsfw = DbNSFW(
        blog_id=blog_id,
        nsfw_prob=probability,
        nsfw_flag=nsfw_flag,
        model_version=model_name,
        model_type=model_type
    )
    db.add(new_nsfw)
    db.commit()
    db.refresh(new_nsfw)
    return new_nsfw
