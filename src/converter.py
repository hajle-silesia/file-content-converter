import abc
import typing
import xml.parsers.expat

import xmltodict

from src.object_factory import ObjectFactory


class Converter(abc.ABC):
    _content_default: typing.ClassVar = {}

    def __init__(self):
        self._content = self._content_default

    @property
    def content(self):
        return self._content

    @abc.abstractmethod
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
            self._content = xmltodict.parse(
                raw_content,
                force_list=(
                    "HOP",
                    "MISC",
                    "FERMENTABLE",
                    "MASH_STEP",
                ),
            )
        except xml.parsers.expat.ExpatError:
            self._content = self._content_default


factory = ObjectFactory()

factory.register_builder("xml", XMLConverter)
