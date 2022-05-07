import threading
from time import sleep
import base64
import json

import requests


class FileContentProcessor(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self, daemon=True)

        self.__monitoring_interval_time = 5
        self.__url = url

        self.__response = None
        self.__raw_content = ""
        self.__content = {}

        self. start()

    @property
    def content(self):
        return self.__content

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
            self.__new_raw_content = json.loads(base64.b64decode(self.__response.json()['content']).decode())
        else:
            self.__new_raw_content = None

    def __update_raw_content(self):
        self.__raw_content = self.__new_raw_content

    def __process_raw_content(self):
        if self.__raw_content:
            self.__content = self.__raw_content
        else:
            self.__content = {}

    def __wait_time_interval(self):
        sleep(self.__monitoring_interval_time)
