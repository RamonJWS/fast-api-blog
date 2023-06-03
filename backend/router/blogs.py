import boto3

from fastapi import File, UploadFile, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from auth.authentication import get_current_active_user
from schemas import BlogPost, DisplayBlogPost, User, ImageResponse
from db.database import get_db
from db import db_blogs, db_ml
from settings import (S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, CENSORED_IMAGE_PATH,
                      NSFW_IMAGE_PATH)
from cloud.s3 import S3Bucket
from ML.nsfw import MLHandler


router = APIRouter(
    tags=['blogs']
)


@router.post("/post")
def create_blog(request: BlogPost,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_active_user)):

    db_session = db

    context_check = MLHandler()
    context_check.make_prediction_content(request.content)

    blogs_response = db_blogs.create_blog(db_session, request, current_user.username)
    db_ml.populate(db_session, blogs_response.id, context_check.prob, context_check.nsfw,
                   context_check.model_name, context_check.model_type)

    try:
        if request.image_metadata is None:
            pass
        elif request.image_metadata["path"].split("/")[-2] == NSFW_IMAGE_PATH:
            request.image_metadata["path"] = CENSORED_IMAGE_PATH
        else:
            db_ml.populate(db_session, blogs_response.id, context_check.prob, context_check.nsfw,
                           context_check.model_name, context_check.model_type)
    except AttributeError:
        pass

    return blogs_response


@router.post("/post/image", response_model=ImageResponse)
def add_image(upload_file: UploadFile = File(...),
              current_user: User = Depends(get_current_active_user)):

    image_check = MLHandler()
    image_check.make_prediction_image(upload_file)

    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             region_name=AWS_REGION
                             )
    s3_bucket = S3Bucket(client=s3_client, username=current_user.username.lower(), bucket_name=S3_BUCKET_NAME)
    s3_bucket.save_image(data=upload_file, nsfw_flag=image_check.nsfw)

    return {"path": s3_bucket.path_on_s3,
            "nsfw_prob": image_check.prob,
            "nsfw_flag": image_check.nsfw,
            "model_name": image_check.model_name
            }


@router.get("/post/all", response_model=List[DisplayBlogPost])
def get_all_blogs(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)):
    return db_blogs.return_all_blogs(db)


@router.delete("/post/{id}")
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_active_user)):

    response = db_blogs.remove_blog(id, db, current_user.username)

    return response
