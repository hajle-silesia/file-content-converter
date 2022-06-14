import base64
import json
import threading

import magic
import requests

from src.converter import factory


class FileContentConverter(threading.Thread):
    _raw_content_default = ""
    _content_default = {}

    def __init__(self, url):
        threading.Thread.__init__(self, daemon=True)

        self.__monitoring_interval_time = 5
        self.__url = url

        self.__raw_content = self._raw_content_default
        self.__content = self._content_default
        self.__response = None

    @property
    def content(self):
        return self.__content

    @property
    def response(self):
        return self.__response

    def update(self, new_raw_content):
        self.__response = None

        if new_raw_content:
            self.__update_raw_content(new_raw_content)
            self.__process_raw_content()
            self.__notify()

    # def __raw_content_changed(self):
    #     self.__get_new_raw_content()
    #
    #     return True if self.__raw_content != self.__new_raw_content else False

    def __update_raw_content(self, new_raw_content):
        self.__raw_content = new_raw_content

    def __process_raw_content(self):
        if self.__raw_content:
            file_type_header = self.__get_file_type_header()
            converter = self.__create_converter(file_type_header)

            if converter:
                converter.process(self.__raw_content)
                self.__content = converter.content
            else:
                self.__content = self.__raw_content

    def __get_file_type_header(self):
        return magic.from_buffer(self.__raw_content.encode())

    def __create_converter(self, file_type_header):
        for file_type in factory.builders:
            if file_type in file_type_header.casefold():
                return factory.create(file_type)

    def __notify(self):
        if self.__content:
            self.__response = requests.post(self.__url, base64.b64encode(json.dumps(self.__content).encode()))
