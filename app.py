import streamlit as st
import requests
import json

from typing import Dict


def get_all_blogs():
    response = requests.get('http://127.0.0.1:8000/post/all')
    data = json.loads(response.text)

    for blog in data:
        st.title(blog['title'])
        st.image(blog['image_url'])
        st.markdown(f"**Content**: {blog['content']}")
        st.markdown(f"**UserID**: {blog['id']}")
        st.markdown(f"**Username**: {blog['username']}")


def create_new_blog(request_body: Dict) -> None:
    json_body = json.dumps(request_body, indent=4)
    response = requests.post('http://127.0.0.1:8000/post', data=json_body)

    if response.ok:
        pass


def add_image_to_blog():
    pass


with st.form("Add new Blog"):
    st.write("Add Post")
    input_username = st.text_input(label="Username")
    input_title = st.text_input(label="Title")
    input_image = st.file_uploader("Image", type=['png', 'jpg'])
    input_content = st.text_input(label="Content")
    submitted = st.form_submit_button("Post")

    if input_image is not None:
        st.empty().image(input_image)

    if submitted:
        st.write(f'Posted: {submitted}')
        data = {
            "user_name": input_username,
            "title": input_title,
            "content": input_content
        }
        create_new_blog(data)

st.button('Get all blogs', on_click=get_all_blogs)
