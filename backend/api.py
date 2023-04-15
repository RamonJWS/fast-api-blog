import shutil
import uvicorn
import os

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated

from settings import API_HOST, API_PORT, ROOT
from schemas import BlogPost, DisplayBlogPost, User, UserInDB
from db.database import get_db, engine
from db import db_blogs, models

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

static_files_path = os.path.join(ROOT, 'files')
app.mount(static_files_path, StaticFiles(directory=static_files_path), name='files')

models.Base.metadata.create_all(engine)


@app.post("/post")
def create_blog_test(request: BlogPost, db: Session = Depends(get_db)):
    return db_blogs.create_blog(db, request)


@app.post("/post/image")
def add_image(title: str, upload_file: UploadFile = File(...)):
    file_name = title.replace(" ", "_") + "_" + upload_file.filename.replace(" ", "_")
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


fake_users_db = {
    "a": {
        "username": "a",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehasheda",
        "disabled": False,
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm =  Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
