"""
Let's get some shared photos!
Using fbchat library: https://fbchat.readthedocs.io/en/stable/api.html#
"""

from distutils import util
import json
import os
from fbchat import Client
from fbchat.models import User, Message, Thread, Attachment
import jsonpickle
from helpers.logger import LOGGER


class Messenger:
    """
    Interact with Users, Messages, Threads and Attachments. Oh my!
    """

    def __init__(self):
        self.__start_client = bool(util.strtobool(os.getenv('START_CLIENT')))
        self.__save_to_file = bool(util.strtobool(os.getenv('SAVE_TO_FILE')))
        LOGGER.debug(self.__save_to_file)
        self.__messages_file_name = os.getenv('FILE_NAME')

        if self.__start_client:
            self.__fb_client = Client(
                os.getenv('USER'), os.getenv('PASS'), max_tries=1)

            if self.__fb_client.isLoggedIn():
                LOGGER.debug('FB Client Logged In!')

    def get_messages(self):
        """
        Get all our messages.
        """

        findme = os.getenv('FINDME')

        all_users = self.__fb_client.fetchAllUsers()
        for user in all_users:
            if user.name == findme:
                LOGGER.debug(f'Found User: {user.name} - ID {user.uid}')

                messages = self.__fb_client.fetchThreadMessages(
                    user.uid, limit=int(os.getenv('THREAD_RETURN_LIMIT')))

                if self.__save_to_file:
                    if os.path.exists(self.__messages_file_name):
                        os.remove(self.__messages_file_name)
                    else:
                        LOGGER.warning(
                            f'The file {self.__messages_file_name} does not exist.')

                    with open(self.__messages_file_name, 'w') as filehandle:
                        json.dump(jsonpickle.encode(messages), filehandle)
                else:
                    return messages

    def get_shared_urls(self):
        """
        Get all our glorious meme urls from the thread messages!
        """

        if self.__save_to_file:
            with open(self.__messages_file_name) as messages_file:
                messages = json.loads(messages_file.read())
            messages = jsonpickle.decode(messages)
        else:
            messages = self.get_messages()

        image_urls = []

        for message in messages:
            if message.attachments:
                for attachment in message.attachments:
                    if hasattr(attachment, 'original_extension'):
                        LOGGER.debug(f'Attachment: {attachment} \n\n')

                        image_meta = {
                            'extension': attachment.original_extension,
                            'url': attachment.large_preview_url
                        }

                        image_urls.append(image_meta)

        return image_urls
