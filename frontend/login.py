import requests
import streamlit as st

from settings import URL

from streamlit import session_state as state


def authentication_header(username: str, password: str) -> dict | None:
    """
    return the authorization bearer from the header if successful authentication
    """

    response = requests.post("http://" + URL + "/token",
                             data={"grant_type": "password", "username": username, "password": password})

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers


def create_account() -> bool:
    """
    return True if account created successfully
    """
    return True


st.title("Login Page")
with st.form("Login"):
    existing_username = st.text_input(label="username")
    existing_password = st.text_input(label="password", type="password")
    submit_login = st.form_submit_button("Login")

    if submit_login:
        header = authentication_header(existing_username, existing_password)
        if header:
            state.header = header
            st.write('**Logged in, you can now access the home page**')
        else:
            st.write('**Login Failed, incorrect username and or password**')

st.title("Create an Account")
with st.form("Create Account"):
    new_username = st.text_input(label="username")
    new_password = st.text_input(label="password", type="password")
    submit_new_login = st.form_submit_button("Create Account")

    if submit_new_login:
        status = create_account()
        if status:
            st.write(f'**Account Created**')
