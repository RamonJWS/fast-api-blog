import pytest
import os

from fastapi.testclient import TestClient

from .test_utils import FakeUser
from settings import ROOT, PROJECT_DIR
from api import app
from db.database import SessionLocal
from db.models import DbBlog, DbUser

automatic_fields = ['timestamp', 'id', 'image_location']
files_dir = os.path.join(ROOT, 'files')
client = TestClient(app)
user = FakeUser("test", "test@gmail.com", "a")


def get_header():
    response = client.post("http://localhost:8000/token",
                           data={"grant_type": "password",
                                 "username": user.username,
                                 "password": user.password})

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def delete_data(request):
    """
    used to delete all data from the blogs and or users table
    """

    table = [i for i in request.param]

    session = SessionLocal()
    if 'blogs' in table:
        session.query(DbBlog).delete()
    if 'users' in table:
        session.query(DbUser).delete()
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
    client.post('/post',
                json={"title": "test title", "content": "test content"},
                headers=get_header())


def test_secret_keys():
    assert os.environ.get("JWT_SECRET_KEY").strip() is not None


@pytest.mark.parametrize("delete_data", [("users", "blogs")], indirect=True)
def test_create_user(delete_data):
    response = client.post('/users/create_account', json={"username": user.username,
                                                          "email": user.email,
                                                          "password": user.password})

    assert response.status_code == 200


@pytest.mark.parametrize("delete_data", [("blogs",)], indirect=True)
def test_authentication(delete_data):
    """
    Authenticate fake user and check they can access a restricted endpoint
    """

    response = client.post("http://localhost:8000/token",
                             data={"grant_type": "password",
                                   "username": user.username,
                                   "password": user.password})

    assert response.status_code == 200


@pytest.mark.parametrize("delete_data", [("blogs",)], indirect=True)
def test_authenticated_user_access(delete_data):
    response = client.get("http://localhost:8000/users/me", headers=get_header())
    assert response.status_code == 200


def test_get_all_blogs():
    response = client.get('/post/all', headers=get_header())
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize("delete_data", [("blogs",)], indirect=True)
def test_create_post_without_image(delete_data):
    response = client.post('/post',
                           json={"title": "test title",
                                 "content": "test content"},
                           headers=get_header())
    assert response.status_code == 200

    testable_response = {k:v for k,v in response.json().items() if k not in ['timestamp', 'id', 'image_location']}

    assert testable_response == {"username": user.username,
                                 "title": "test title",
                                 "content": "test content"}


def test_delete_post_without_image(fake_data):

    user_id = 1
    response = client.delete(f'/post/{user_id}', headers=get_header())
    assert response.status_code == 200


@pytest.mark.parametrize("delete_data", [("blogs",)], indirect=True)
def test_create_image(delete_data):

    with open(os.path.join(PROJECT_DIR,'readme_files/api.png'), 'rb') as f:

        response = client.post('/post/image',
                               files={'upload_file': ("api.png", f, "image/png")},
                               params={"title": "test title"},
                               headers=get_header())

    assert response.status_code == 200


@pytest.mark.parametrize("delete_data", [("blogs",)], indirect=True)
def test_create_post_with_image(delete_data):

    with open(os.path.join(PROJECT_DIR, 'readme_files/api.png'), 'rb') as f:

        response_image = client.post('/post/image',
                                     files={'upload_file': ("api.png", f, "image/png")},
                                     params={"title": "test title"},
                                     headers=get_header())

    response = client.post('/post', json={"title": "test title",
                                          "content": "test content",
                                          "image_location": response_image.text.replace('"', '')},
                           headers=get_header())

    assert response.status_code == 200

    testable_response = {k:v for k,v in response.json().items() if k not in ['timestamp', 'id']}

    assert testable_response == {"username": user.username,
                                 "title": "test title",
                                 "content": "test content",
                                 "image_location": response_image.text.replace('"', '')}