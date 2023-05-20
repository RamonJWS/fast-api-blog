import os

from dotenv import load_dotenv

load_dotenv()

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(ROOT)

API_HOST = '127.0.0.1'
API_PORT = 8000
SQLALCHEMY_DATABASE_DIR = 'sqlite:///' + os.path.join(ROOT, 'blog.db')

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = "eu-west-2"
S3_BUCKET_NAME = "fast-api-blog-images"
