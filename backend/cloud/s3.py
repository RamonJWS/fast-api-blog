import boto3
import os

from fastapi import UploadFile
from datetime import datetime

from utils.regex import replace_special_characters

FLAGGED_FOLDER = "Flagged_NSFW"


class S3Bucket:
    def __init__(self, client: boto3.client, username: str, bucket_name: str):
        self.s3_client = client
        self.user_folder_name = username
        self.bucket_name = bucket_name

        self.path_on_s3: str = ""

    def save_image(self, data: UploadFile, nsfw_flag: bool = False) -> None:
        time_stamp = replace_special_characters(str(datetime.utcnow().replace(microsecond=0)), "_")
        file_name = time_stamp + '_' + data.filename
        if nsfw_flag:
            self.path_on_s3 = os.path.join(self.user_folder_name, FLAGGED_FOLDER, file_name)
        else:
            self.path_on_s3 = os.path.join(self.user_folder_name, file_name)
        self.s3_client.put_object(Bucket=self.bucket_name, Key=self.path_on_s3, Body=data.file)
