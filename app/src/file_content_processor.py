import threading
from time import sleep
import base64
import magic

import requests

from app.src.converter import factory


class FileContentProcessor(threading.Thread):
    _content_default = {}

    def __init__(self, url):
        threading.Thread.__init__(self, daemon=True)

        self.__monitoring_interval_time = 5
        self.__url = url

        self.__response = None
        self.__raw_content = ""
        self.__content = self._content_default

        self. start()

    @property
    def content(self):
        return self.__content

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    def run(self):
        while True:
            self.__monitor_raw_content()

    def __monitor_raw_content(self):
        if self.__raw_content_changed():
            self.__update_raw_content()
            self.__process_raw_content()

        self.__wait_time_interval()

    def __raw_content_changed(self):
        self.__get_new_raw_content()

        return True if self.__raw_content != self.__new_raw_content else False

    def __get_new_raw_content(self):
        self.__get_response()
        self.__extract_new_raw_content()

    def __get_response(self):
        self.__response = requests.get(self.__url)

    def __extract_new_raw_content(self):
        if self.__response.status_code == 200:
            self.__new_raw_content = base64.b64decode(self.__response.json()['content']).decode()
        else:
            self.__new_raw_content = None

    def __update_raw_content(self):
        self.__raw_content = self.__new_raw_content

    def __process_raw_content(self):
        if self.__raw_content:
            # file_type = self.__get_file_type()
            # converter = self.__factory.create(file_type)
            # converter.process()
            file_type_header = magic.from_buffer(self.__raw_content.encode())

            for file_type in factory.builders:
                if file_type in file_type_header.casefold():
                    break
            try:
                converter = factory.create(file_type)
            except ValueError:
                print(f"File type {file_type} not supported")
            converter.process(self.__raw_content)
            self.__content = converter.content
        else:
            self.__content = self._content_default

    def __wait_time_interval(self):
        sleep(self.__monitoring_interval_time)
