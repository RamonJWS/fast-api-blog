import streamlit as st
import requests
import json

def get_all_blogs():
    response = requests.get('http://127.0.0.1:8000/post/all')
    data = json.loads(response.text)
    for blog in data:
        st.title(blog['title'])
        st.image(blog['image_url'])
        st.markdown(f"**Content**: {blog['content']}")
        st.markdown(f"**UserID**: {blog['id']}")
        st.markdown(f"**Username**: {blog['username']}")

st.button('Get all blogs', on_click=get_all_blogs)

