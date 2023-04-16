import shutil
import os

from fastapi import File, UploadFile, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from auth.authentication import get_current_active_user
from schemas import BlogPost, DisplayBlogPost, User
from db.database import get_db
from db import db_blogs


router = APIRouter(
    tags=['blogs']
)


@router.post("/post")
def create_blog_test(request: BlogPost,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_active_user)):
    return db_blogs.create_blog(db, request)


@router.post("/post/image")
def add_image(title: str,
              upload_file: UploadFile = File(...),
              current_user: User = Depends(get_current_active_user)):
    file_name = title.replace(" ", "_") + "_" + upload_file.filename.replace(" ", "_")
    path = os.path.join("files", file_name)

    # save image locally
    with open(path, "w+b") as file:
        shutil.copyfileobj(upload_file.file, file)

    return path


@router.get("/post/all", response_model=List[DisplayBlogPost])
def get_all_blogs(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)):
    return db_blogs.return_all_blogs(db)


@router.delete("/post/{id}")
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_active_user)):

    # remove post image
    image_urls = db_blogs.return_all_image_urls(db)
    for url, post_id in image_urls:
        if url:
            if post_id == id:
                path = "/".join(url.split("/")[-2:])
                try:
                    os.remove(path)
                except FileNotFoundError:
                    pass

    return db_blogs.remove_blog(id, db)