# About
I wanted to create a simple blog post website that allows for users to view all the current blogs,
post their own blogs and delete blogs. This is a simple learning project and is NOT designed for real
life applications.

![Alt Text](readme_files/demo.gif)

## Overview

**Tech Stack**:

- Language: Python
- API: FastAPI
- Frontend: Streamlit
- Database: Sqlite

**Home Page**

The image below shows the home page for the website, it contains all the current blogs in the database.
The is a new blog is added it will immediately show up here, no need for refreshing.

![My text](readme_files/home_page.png)

**Create Post**

To create a new post the `Create Post` tab can be used. Users can add images to their posts if they 
want. Each new post is given a unique ID in the 
backend and the contents is saved in the `Blogs` table, the images are saved as static files and their
URLs are saved in the `Blogs` table.

![My Image](readme_files/create.png)

**Delete Post**

Posts can be deleted by anyone (hence not production ready), the post id needs to be referenced so the 
backend knows what post to delete. When deleting a post a delete image method is also called, this will
only apply to posts with images.

![My Image](readme_files/delete.png)
## API:

The API was built using FastAPI with the following endpoints:

![My Image](readme_files/api.png)

## Try it out yourself:

Make sure python is installed.

1. `git clone https://github.com/RamonJWS/fast-api-blog.git`
2. `cd fast-api-blog.git`
3. `python -m venv blogvenv`
4. MacOS: `source blogvenv/bin/activate` or Windows: `blogvenv\Scripts\activate`
5. `pip install -r requirements.txt`
6. `streamlit run streamlit_app.py` (default runs on port 8501)
7. open another terminal
8. `uvicorn api:app --reload` (runs on port 8000)

The backend will create a local db called blog.db, this is a sqlite database which can be viewed with
TablePlus if needed.

## Improvements:

- Add in authentication and user roles.
- Only allow users who created blogs to delete their own blogs.
- Add in comments and voting system.
- Deploy to AWS. Ideally S3 bucket for static website and EC2 for backend.