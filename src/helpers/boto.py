"""
Upload to AWS S3
"""

import io
import os
import boto3
import requests
from helpers.logger import LOGGER


class S3:
    """
    S3 Stuff.
    """

    def __init__(self):
        self.__s3_client = boto3.resource('s3', aws_access_key_id=os.getenv(
            'ACCESS_KEY'), aws_secret_access_key=os.getenv('SECRET_KEY'))
        self.__bucket = self.__s3_client.Bucket(
            f"{os.getenv('APP')}-{os.getenv('S3_BUCKET')}")

    def create_bucket(self):
        """
        Grab files from the list of urls passed and save to S3. YAAAR!
        """

        response = self.__bucket.create(
            ACL='public-read'
        )

        LOGGER.debug(
            f"Bucket Status: {response['ResponseMetadata']['HTTPStatusCode']} | Bucket Location: {response['Location']}")

    def upload_files(self, image_urls):
        """
        Upload dem filez...
        """

        file_count = 0
        for meta in image_urls:
            file_count += 1

            if not meta.get('url') is None:
                meme_file = requests.get(meta.get('url'))
                response = self.__bucket.upload_fileobj(
                    io.BytesIO(meme_file.content), f"meme-gold-{file_count}.{meta.get('extension')}", ExtraArgs={'ACL': 'public-read'})

                LOGGER.debug(response)

                LOGGER.info(f"meme-gold-{file_count}.{meta.get('extension')}")
