import os
import argparse

from dotenv import load_dotenv

load_dotenv()
IP = os.getenv("LOCAL_IP")
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = "fast-api-blog-images"


parser = argparse.ArgumentParser(description='Your script description')
parser.add_argument('--LOCAL', action='store_true', help='Enable debug mode')
args = parser.parse_args()

if args.LOCAL:
    URL = "127.0.0.1:8000"
else:
    URL = "35.177.193.119:80"
