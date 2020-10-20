"""
We be searching for meme gold lads!
"""

from helpers.boto import S3
from helpers.facebook import Messenger

FB_MESSENGER = Messenger()
S3_BOTO = S3()

FB_MESSENGER.get_messages()

S3_BOTO.create_bucket()
S3_BOTO.upload_files(FB_MESSENGER.get_shared_urls())
