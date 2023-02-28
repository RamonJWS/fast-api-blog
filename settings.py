import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(ROOT)

SQLALCHEMY_DATABASE_DIR = 'sqlite:///' + os.path.join(ROOT, 'blog.db')
