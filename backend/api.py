import shutil
import uvicorn
import os

from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

from settings import API_HOST, API_PORT
from schemas import BlogPost, DisplayBlogPost
from db.database import get_db, engine
from db import db_blogs, models

app = FastAPI()
app.mount('/files', StaticFiles(directory='files'), name='files')

models.Base.metadata.create_all(engine)


@app.post("/post")
def create_blog_test(request: BlogPost, db: Session = Depends(get_db)):
    return db_blogs.create_blog(db, request)


@app.post("/post/image")
def add_image(title: str, upload_file: UploadFile = File(...)):
    file_name = title + "_" + upload_file.filename
    path = os.path.join("files", file_name)

    # save image locally
    with open(path, "w+b") as file:
        shutil.copyfileobj(upload_file.file, file)

    return path


@app.get("/post/all", response_model=List[DisplayBlogPost])
def get_all_blogs(db: Session = Depends(get_db)):
    return db_blogs.return_all_blogs(db)


@app.delete("/post/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):

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


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
