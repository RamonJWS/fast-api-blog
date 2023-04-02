# About
**Tech Stack**: Python, FastAPI, EC2, Docker, Streamlit, SqlAlchemy, Sqlite.

I wanted to create a simple blog post website that allows for users to view all the current blogs,
post their own blogs and delete blogs. This is a simple learning project and is NOT designed for real
life applications as there is no authentication or user accounts meaning that anyone can delete any post.

The site can be found here: http://ec2-13-53-56-159.eu-north-1.compute.amazonaws.com/

(note: this site will not remain active as it could be used for inappropriate content.)

![Alt Text](readme_files/demo.gif)

## Overview

**Home Page**

The image below shows the home page for the website, it contains all the current blogs in the database.
If a new blog is added it will immediately show up here, no need for refreshing.

![My text](readme_files/home_page.png)

**Create Post**

Use the `Create Post` tab to create a new post. Users have the option to add images to their posts. Each new post
is given a unique ID in the backend and the contents is saved in the `Blogs` table, the images are saved as static
files and their URLs are saved in the `Blogs` table.

![My Image](readme_files/create.png)

**Delete Post**

Posts can be deleted by anyone (hence not production ready), the post id needs to be referenced so the 
backend knows what post to delete. When deleting a post a delete image method is also called, this will
only apply to posts with images.

![My Image](readme_files/delete.png)
## API:

The API was built using FastAPI with the following endpoints:

![My Image](readme_files/api.png)

## Run it locally:

Make sure docker and python is installed (using python 3.11)

1. `git clone https://github.com/RamonJWS/fast-api-blog`
2. `cd fast-api-blog`
3. `docker-compose up -d`
4. Open a web browser and type in `localhost:8501`

The backend will create a local db called blog.db, this is a sqlite database which can be viewed with
TablePlus if needed.

## Improvements:

- Add in async await for concurrent jobs.
- Add in user accounts and authentication.
- Only allow creator or admin of blog to delete blog post.
- Add in inappropriate image and text classifier to remove explicit content.