from abc import ABC, abstractmethod
from xml.parsers.expat import ExpatError, errors

import xmltodict

from app.src.object_factory import ObjectFactory


class Converter(ABC):
    def __init__(self):
        self._content = {}

    @property
    def content(self):
        return self._content

    @abstractmethod
    def process(self, raw_content):
        pass


class XMLConverter(Converter):
    def process(self, raw_content):
        if raw_content:
            self.__parse(raw_content)

    def __parse(self, raw_content):
        try:
            self._content = xmltodict.parse(raw_content)
        except ExpatError as err:
            print(f"Parsing error code {err.code}: {errors.messages[err.code]}")


factory = ObjectFactory()

factory.register_builder('xml', XMLConverter)
