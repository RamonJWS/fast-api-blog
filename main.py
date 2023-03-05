import shutil
import uvicorn
import os

from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from schemas import BlogPost
from db.database import get_db, engine
from db import db_blogs
from db import models

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.post("/post")
def create_blog_test(blog: BlogPost, db: Session = Depends(get_db)):
    return db_blogs.create_blog(db, blog)


@app.post("/post/image", response_class=FileResponse)
def add_image(id: int, upload_file: UploadFile = File(...)):
    path = os.path.join("files", str(id) + "_" + upload_file.filename)

    # check image exists for id, if so remove it.
    files_start_with_id = [file for file in os.listdir("files") if file.startswith(str(id))]
    if files_start_with_id:
        for file in files_start_with_id:
            os.remove(os.path.join('files', file))

    # save image locally

    with open(path, "w+b") as file:
        shutil.copyfileobj(upload_file.file, file)
    return path


@app.get("/post/all")
def get_all_blogs(db: Session = Depends(get_db)):
    return db_blogs.return_all_blogs(db)


@app.delete("/post/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    return db_blogs.remove_blog(id, db)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)