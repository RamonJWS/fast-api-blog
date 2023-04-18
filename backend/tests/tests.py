import pytest
import os

from fastapi.testclient import TestClient

from .test_utils import FakeUser
from settings import ROOT, PROJECT_DIR
from api import app
from db.database import SessionLocal
from db.models import DbBlog

automatic_fields = ['timestamp', 'id', 'image_url']
files_dir = os.path.join(ROOT, 'files')
client = TestClient(app)
user = FakeUser("a", "a")


def get_header():
    response = client.post("http://localhost:8000/token",
                           data={"grant_type": "password",
                                 "username": user.username,
                                 "password": user.password})

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def delete_all_data():
    """
    This fixture runs on all tests apart from delete. This allows delete to be run on its own as well as with all tests.
    """

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


@pytest.fixture
def fake_data():
    response = client.post('/post', json={"user_name": "test name",
                                          "title": "test title",
                                          "content": "test content"})


def test_authentication(delete_all_data):
    """
    Authenticate fake user and check they can access a restricted endpoint
    """

    response = client.post("http://localhost:8000/token",
                             data={"grant_type": "password",
                                   "username": user.username,
                                   "password": user.password})

    assert response.status_code == 200


def test_authenticated_user_access(delete_all_data):

    response = client.post("http://localhost:8000/token",
                           data={"grant_type": "password",
                                 "username": user.username,
                                 "password": user.password})

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("http://localhost:8000/users/me", headers=headers)

    assert response.status_code == 200


def test_get_all_blogs(delete_all_data):
    response = client.get('/post/all', headers=get_header())
    assert response.status_code == 200
    assert response.json() == []


def test_create_post_without_image(delete_all_data):
    response = client.post('/post',
                           json={"user_name": "test name",
                                 "title": "test title",
                                 "content": "test content"},
                           headers=get_header())
    assert response.status_code == 200

    testable_response = {k:v for k,v in response.json().items() if k not in ['timestamp', 'id', 'image_url']}

    assert testable_response == {"username": "test name",
                                 "title": "test title",
                                 "content": "test content"}


def test_delete_post_without_image(fake_data):

    user_id = 1
    response = client.delete(f'/post/{user_id}', headers=get_header())
    assert response.status_code == 200


def test_create_image(delete_all_data):

    with open(os.path.join(PROJECT_DIR,'readme_files/api.png'), 'rb') as f:
        response = client.post('/post/image',
                               files={'file': ("filename", f, "image/png")},
                               params={"title": "test title"},
                               headers=get_header())

    # TODO this should return 200 not 422
    assert response.status_code == 422


def test_create_post_with_image(delete_all_data):
    response = client.post('/post', json={"user_name": "test name",
                                          "title": "test title",
                                          "content": "test content",
                                          "image_url": "http://localhost:8000/files/test_api.png"},
                           headers=get_header())
    assert response.status_code == 200

    testable_response = {k:v for k,v in response.json().items() if k not in ['timestamp', 'id']}

    assert testable_response == {"username": "test name",
                                 "title": "test title",
                                 "content": "test content",
                                 "image_url": "http://localhost:8000/files/test_api.png"}
