import os

import streamlit as st
import requests
import json

from typing import Dict
from dotenv import load_dotenv

from settings import URL

load_dotenv()
IP = os.getenv("LOCAL_IP")


def get_all_blogs():
    response = requests.get('http://' + URL + '/post/all')
    blog_data = json.loads(response.text)

    for blog in blog_data:
        st.title(blog['title'])
        if blog['image_url']:
            st.image(blog['image_url'])
        st.markdown(f"**Content**: {blog['content']}")
        st.markdown(f"**Post ID**: {blog['id']}")
        st.markdown(f"**Username**: {blog['username']}")


def create_new_blog(request_body: Dict) -> None:
    json_body = json.dumps(request_body, indent=4)
    response = requests.post('http://' + URL + '/post', data=json_body)

    if response.ok:
        pass


def add_image_to_blog(title: str, img) -> str:
    query_params = {"title": title}
    files = {"upload_file": img}
    response = requests.post('http://' + URL + '/post/image', params=query_params, files=files)

    if response.ok:
        return response.text.replace('"', '')


def delete_post(id: int) -> None:
    response = requests.delete(f'http://' + URL + '/post/{id}')

    if response.ok:
        pass


# Create tabs
tabs = ["Home Page", "Create Post", "Delete Post"]
home, post, delete = st.tabs(["Home Page", "Create Post", "Delete Post"])

with post:
    with st.form("Add new Blog"):
        st.write("Add Post")
        input_username = st.text_input(label="Username")
        input_title = st.text_input(label="Title")
        input_image = st.file_uploader("Image", type=['png', 'jpeg'])
        input_content = st.text_input(label="Content")
        submitted = st.form_submit_button("Post")

        if submitted:
            if input_image is not None:
                response_body = add_image_to_blog(input_title, input_image)

                data = {
                    "user_name": input_username,
                    "title": input_title,
                    "content": input_content,
                    "image_url": "http://" + URL + "/" + response_body
                }

            else:
                data = {
                    "user_name": input_username,
                    "title": input_title,
                    "content": input_content
                }

            create_new_blog(data)
            st.write(f'Posted: {submitted}')

with delete:
    with st.form("Delete Post"):
        st.write("Delete a Post")
        delete_id = st.text_input(label="Post ID")
        submitted = st.form_submit_button("Delete!")

        if submitted:
            delete_post(int(delete_id))
            st.write(f"Post with ID {delete_id} deleted")

with home:
    get_all_blogs()
