import boto3
import os

from fastapi import UploadFile
from datetime import datetime

from utils.regex import replace_special_characters


class S3Bucket:
    def __init__(self, session: boto3.Session, username: str, bucket_name: str):
        self.s2_session = session
        self.user_folder_name = username
        self.bucket_name = bucket_name

        self.path_on_s3: str = ""

    def save_image(self, s3: boto3.client, data: UploadFile) -> None:
        time_stamp = replace_special_characters(str(datetime.utcnow().replace(microsecond=0)), "_")
        file_name = time_stamp + '_' + data.filename
        self.path_on_s3 = os.path.join(self.user_folder_name, file_name)
        s3.put_object(Bucket=self.bucket_name, Key=self.path_on_s3, Body=data.file)
