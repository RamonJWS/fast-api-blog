import requests
import re
import json
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
        state.header = headers
        return headers


def create_account(username: str, email: str, password: str) -> dict:
    """
    return True if account created successfully
    """
    json_body = json.dumps({"username": username, "email": email, "password": password}, indent=4)
    response = requests.post("http://" + URL + "/users/create_account",
                             data=json_body)
    return response.json()


def email_validation(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False


def valid_username(name: str) -> bool:
    if re.match("^\\w+$", name):
        return True
    return False


st.title("Login Page")
with st.form("Login"):
    existing_username = st.text_input(label="username")
    existing_password = st.text_input(label="password", type="password")
    submit_login = st.form_submit_button("Login")

    if submit_login:
        header = authentication_header(existing_username, existing_password)
        if header:
            st.write('**Logged in, you can now access the home page**')
        else:
            st.error('**Login Failed, incorrect username and or password**')

st.title("Create an Account")
with st.form("Create Account"):
    new_username = st.text_input(label="username")
    new_email = st.text_input(label="email")
    new_password = st.text_input(label="password", type="password")
    submit_new_login = st.form_submit_button("Create Account")

    if submit_new_login:
        if new_username and new_email and new_password:
            if valid_username(new_username):
                if email_validation(new_email):
                    response = create_account(new_username, new_email, new_password)
                    if 'detail' in response:
                        st.error(response['detail'])
                    else:
                        st.write(f'**Account Created for:**')
                        st.write(f'user: {response["username"]}')
                        st.write(f'email: {response["email"]}')
                        authentication_header(new_username, new_password)
                else:
                    st.error("Please enter a valid email.")
            else:
                st.error("Usernames can't use special characters")
        else:
            st.error("Please ensure all the fields are filled in.")
