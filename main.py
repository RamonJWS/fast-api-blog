import shutil
import uvicorn

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from schemas import BlogPost


app = FastAPI()

fake_db = []

@app.post("/post")
def create_blog_test(blog: BlogPost):

    if not fake_db:
        blog_id = 0
    else:
        blog_id = fake_db[-1]["blog_id"] + 1

    fake_db.append({"user_name": blog.user_name,
                    "title": blog.title,
                    "content": blog.content,
                    "blog_id": blog_id})

    return {
        "blog": blog
    }


@app.post("/post/image", response_class=FileResponse)
def add_image(upload_file: UploadFile = File(...)):
    path = f"files/{upload_file.filename}"
    with open(path, "w+b") as file:
        shutil.copyfileobj(upload_file.file, file)

    return path


@app.get("/post/all")
def get_all_blogs():
    return {
        "data": fake_db
    }


@app.delete("/post/{id}")
def delete_post(id: int):
    fake_db.pop(id)
    return {
        "data": fake_db
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)