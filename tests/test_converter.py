import pathlib
import unittest

from src.converter import XMLConverter


class TestConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_expected_results()

    @classmethod
    def set_test_arguments(cls):
        cls.empty_raw_content = ""
        cls.header_only_raw_content = "<?xml version='1.0' encoding='UTF-8'?>"
        with (pathlib.Path(__file__).parent / "./files/converter.xml").open(encoding="utf-8") as file:
            cls.nonempty_raw_content = file.read()

    @classmethod
    def set_tested_objects(cls):
        cls.xml_converter = XMLConverter()

    @classmethod
    def set_expected_results(cls):
        cls.expected_empty_content = {}
        cls.expected_nonempty_content = {
            "note": {
                "to": "Smith",
                "from": "Adams",
                "heading": "Test",
                "body": "Test body",
            },
        }

    def test_should_get_empty_content_when_given_empty_raw_content(self):
        self.xml_converter.process(self.empty_raw_content)

        assert self.expected_empty_content == self.xml_converter.content

    def test_should_get_empty_content_when_given_header_only_raw_content(self):
        self.xml_converter.process(self.header_only_raw_content)

        assert self.expected_empty_content == self.xml_converter.content

    def test_should_get_nonempty_content_when_given_nonempty_raw_content(self):
        self.xml_converter.process(self.nonempty_raw_content)

        assert self.expected_nonempty_content == self.xml_converter.content

    def test_should_get_empty_content_when_given_empty_raw_content_becomes_header_only(self):
        self.xml_converter.process(self.empty_raw_content)
        self.xml_converter.process(self.header_only_raw_content)

        assert self.expected_empty_content == self.xml_converter.content

    def test_should_get_nonempty_content_when_given_header_only_raw_content_becomes_nonempty(self):
        self.xml_converter.process(self.header_only_raw_content)
        self.xml_converter.process(self.nonempty_raw_content)

        assert self.expected_nonempty_content == self.xml_converter.content

    def test_should_get_nonempty_content_when_given_empty_raw_content_becomes_nonempty(self):
        self.xml_converter.process(self.empty_raw_content)
        self.xml_converter.process(self.nonempty_raw_content)

        assert self.expected_nonempty_content == self.xml_converter.content

    def test_should_get_empty_content_when_given_nonempty_raw_content_becomes_header_only(self):
        self.xml_converter.process(self.nonempty_raw_content)
        self.xml_converter.process(self.header_only_raw_content)

        assert self.expected_empty_content == self.xml_converter.content

    def test_should_get_empty_content_when_given_header_only_raw_content_becomes_empty(self):
        self.xml_converter.process(self.header_only_raw_content)
        self.xml_converter.process(self.empty_raw_content)

        assert self.expected_empty_content == self.xml_converter.content

    def test_should_get_empty_content_when_given_nonempty_raw_content_becomes_empty(self):
        self.xml_converter.process(self.nonempty_raw_content)
        self.xml_converter.process(self.empty_raw_content)

        assert self.expected_empty_content == self.xml_converter.content
