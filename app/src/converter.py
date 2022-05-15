from abc import ABC, abstractmethod
from xml.parsers.expat import ExpatError

import xmltodict

from app.src.object_factory import ObjectFactory


class Converter(ABC):
    _content_default = {}

    def __init__(self):
        self._content = self._content_default

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
        else:
            self._content = self._content_default

    def __parse(self, raw_content):
        try:
            self._content = xmltodict.parse(raw_content)
        except ExpatError:
            self._content = self._content_default


factory = ObjectFactory()

factory.register_builder('xml', XMLConverter)
