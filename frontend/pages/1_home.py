import http
import boto3

import streamlit as st
import requests
import json

from io import BytesIO
from PIL import Image
from typing import Dict
from streamlit import session_state as state

from settings import URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, AWS_REGION

# API endpoints
ALL_BLOGS_ENDPOINT = f'http://{URL}/post/all'
CREATE_BLOG_ENDPOINT = f'http://{URL}/post'
ADD_IMAGE_ENDPOINT = f'http://{URL}/post/image'
DELETE_BLOG_ENDPOINT = f'http://{URL}/post'


def get_image_from_s3(image_key: str) -> Image:
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION
                      )
    response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=image_key)
    image_data = response['Body'].read()
    return Image.open(BytesIO(image_data))


def get_all_blogs():
    response = requests.get(ALL_BLOGS_ENDPOINT, headers=state.header)
    if response.status_code == 200:
        blog_data = json.loads(response.text)

        for blog in blog_data:
            st.title(blog['title'])
            if blog['image_location']:
                st.image(get_image_from_s3(blog['image_location']))
            st.markdown(f"{blog['content']}")
            st.markdown(f"Post ID: **{blog['id']}**")
            st.markdown(f"Username: **{blog['username']}**")
    else:
        st.error(f"Failed to retrieve posts with status code {response.status_code}")


def create_new_blog(request_body: Dict) -> int:
    json_body = json.dumps(request_body, indent=4)
    response = requests.post(CREATE_BLOG_ENDPOINT, data=json_body, headers=state.header)
    if response.status_code == 200:
        return response.status_code
    else:
        st.error(f"Failed to create post with status code {response.status_code}")


def add_image_to_blog(title: str, img) -> str:
    query_params = {"title": title}
    files = {"upload_file": img}
    response = requests.post(ADD_IMAGE_ENDPOINT, params=query_params, files=files, headers=state.header)

    if response.ok:
        return response.text.replace('"', '')
    else:
        st.error(f"Failed to add image to post with status code {response.status_code}")


def delete_post(id: int):

    try:
        int(id)
    except ValueError:
        st.error("Invalid entry, make sure the ID is an integer.")
        return

    response = requests.delete(f'{DELETE_BLOG_ENDPOINT}/{id}', headers=state.header)
    if response.status_code == 200:
        st.write(f"Post with ID {delete_id} deleted")
    elif response.status_code == http.HTTPStatus.NOT_FOUND:
        st.error(f"Failed to delete post. The post either doesn't exist or you're not the author")


# user needs to have logged in before accessing the following resources
if 'header' in state:

    # Create tabs
    tabs = ["Home Page", "Create Post", "Delete Post"]
    home, post, delete = st.tabs(["Home Page", "Create Post", "Delete Post"])

    with post:
        with st.form("Add new Blog"):
            st.write("Add Post")
            input_title = st.text_input(label="Title")
            input_image = st.file_uploader("Image", type=['png', 'jpeg'])
            input_content = st.text_input(label="Content")
            submitted = st.form_submit_button("Post")

            if submitted:
                if input_image is not None:
                    response_body = add_image_to_blog(input_title, input_image)

                    data = {
                        "title": input_title,
                        "content": input_content,
                        "image_location": f"{response_body}"
                    }

                else:
                    data = {
                        "title": input_title,
                        "content": input_content
                    }

                status = create_new_blog(data)
                if status == 200:
                    st.write(f'Posted: {submitted}')
                elif status == 401:
                    st.write(f'Error unauthorized request')

    with delete:
        with st.form("Delete Post"):
            st.write("Delete a Post")
            delete_id = st.text_input(label="Post ID")
            submitted = st.form_submit_button("Delete!")

            if submitted:
                delete_post(delete_id)

    with home:
        get_all_blogs()

else:
    st.error("You need to be logged in to access this page")
