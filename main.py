import shutil
import uvicorn
import os

from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from schemas import BlogPost, DisplayBlogPost
from db.database import get_db, engine
from db import db_blogs
from db import models

app = FastAPI()
app.mount('/files', StaticFiles(directory='files'), name='files')

models.Base.metadata.create_all(engine)

# frontend port (needed as frontend and backend are on same machine)
# origins = [
#     'http://localhost:3000'
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     low_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*']
# )

@app.post("/post")
def create_blog_test(request: BlogPost, db: Session = Depends(get_db)):
    return db_blogs.create_blog(db, request)


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


@app.get("/post/all", response_model=List[DisplayBlogPost])
def get_all_blogs(db: Session = Depends(get_db)):
    return db_blogs.return_all_blogs(db)


@app.delete("/post/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    return db_blogs.remove_blog(id, db)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
