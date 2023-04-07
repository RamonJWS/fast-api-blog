import pytest
import os

from fastapi.testclient import TestClient

from settings import ROOT, PROJECT_DIR
from api import app
from db.database import SessionLocal
from db.models import DbBlog

automatic_fields = ['timestamp', 'id', 'image_url']
files_dir = os.path.join(ROOT, 'files')

client = TestClient(app)


@pytest.fixture(scope='session', autouse=True)
def delete_all_data():

    # clean db
    session = SessionLocal()
    session.query(DbBlog).delete()
    session.commit()
    session.close()

    # clean dir with images
    if os.path.exists(files_dir):
        all_image_files = os.listdir(files_dir)
        for file in all_image_files:
            if file != '.gitkeep':
                os.remove(os.path.join(files_dir, file))


def test_get_all_blogs():
    response = client.get('/post/all')
    assert response.status_code == 200
    assert response.json() == []

def test_create_post_without_image():
    response = client.post('/post', json={"user_name": "test name",
                                          "title": "test title",
                                          "content": "test content"})
    assert response.status_code == 200

    testable_response = {k:v for k,v in response.json().items() if k not in ['timestamp', 'id', 'image_url']}

    assert testable_response == {"username": "test name",
                                 "title": "test title",
                                 "content": "test content"}

def test_delete_post_without_image():
    user_id = 1
    response = client.delete(f'/post/{user_id}')
    assert response.status_code == 200


def test_create_image():

    with open(os.path.join(PROJECT_DIR,'readme_files/api.png'), 'rb') as f:
        response = client.post('/post/image',
                               files={'file': ("filename", f, "image/png")},
                               params={"title": "test title"})

    assert response.status_code == 422


def test_create_post_with_image():
    response = client.post('/post', json={"user_name": "test name",
                                          "title": "test title",
                                          "content": "test content",
                                          "image_url": "http://localhost:8000/files/test_api.png"})
    assert response.status_code == 200

    testable_response = {k:v for k,v in response.json().items() if k not in ['timestamp', 'id']}

    assert testable_response == {"username": "test name",
                                 "title": "test title",
                                 "content": "test content",
                                 "image_url": "http://localhost:8000/files/test_api.png"}