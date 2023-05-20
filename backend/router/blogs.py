import shutil
import os
import boto3

from fastapi import File, UploadFile, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from auth.authentication import get_current_active_user
from schemas import BlogPost, DisplayBlogPost, User
from db.database import get_db
from db import db_blogs
from settings import S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from cloud.s3 import S3Bucket


router = APIRouter(
    tags=['blogs']
)


@router.post("/post")
def create_blog(request: BlogPost,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_active_user)):
    return db_blogs.create_blog(db, request, current_user.username)


@router.post("/post/image")
def add_image(upload_file: UploadFile = File(...),
              current_user: User = Depends(get_current_active_user)):

    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             region_name=AWS_REGION
                             )
    s3_bucket = S3Bucket(client=s3_client, username=current_user.username.lower(), bucket_name=S3_BUCKET_NAME)
    s3_bucket.save_image(data=upload_file)

    return s3_bucket.path_on_s3


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
