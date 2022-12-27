import magic

from src.converter import factory


class FileContentConverter:
    _raw_content_default = ""
    _content_default = {}

    def __init__(self, producer):
        self.__producer = producer

        self.__raw_content = self._raw_content_default
        self.__content = self._content_default

    @property
    def content(self):
        return self.__content

    def update(self, new_raw_content):
        self.__update_raw_content(new_raw_content)
        self.__process_raw_content()
        self.__notify()

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
        if self.content:
            self.__producer.send(topic="file-content-converter-topic",
                                 value=self.content,
                                 )
