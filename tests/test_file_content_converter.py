import pathlib
import unittest.mock

from src.file_content_converter import FileContentConverter


class MockProducer:
    def send(self, topic, value):
        pass


class TestFileContentConverter(unittest.TestCase):
    producer = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.nonempty_content = "test_content"
        cls.xml_header_only_raw_content = "<?xml version='1.0' encoding='UTF-8'?>"
        with (pathlib.Path(__file__).parent / "./files/converter.xml").open(encoding="utf-8") as file:
            cls.xml_nonempty_raw_content = file.read()

        cls.producer = MockProducer()

        cls.expected_xml_nonempty_content = {
            "note": {
                "to": "Smith",
                "from": "Adams",
                "heading": "Test",
                "body": "Test body",
            },
        }

    def setUp(self):
        super().setUp()

        self.file_content_converter = FileContentConverter(self.producer)

    def test_should_get_empty_content_when_given_none_raw_content(self):
        self.file_content_converter.update(None)

        assert self.file_content_converter.content == {}

    def test_should_get_empty_content_when_none_raw_content_becomes_empty_raw_content(self):
        self.file_content_converter.update(None)
        self.file_content_converter.update("")

        assert self.file_content_converter.content == {}

    def test_should_get_empty_content_when_given_empty_raw_content(self):
        self.file_content_converter.update("")

        assert self.file_content_converter.content == {}

    def test_should_get_content_when_empty_raw_content_becomes_nonempty_raw_content(self):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.nonempty_content)

        assert self.nonempty_content == self.file_content_converter.content

    def test_should_get_content_when_given_nonempty_raw_content(self):
        self.file_content_converter.update(self.nonempty_content)

        assert self.nonempty_content == self.file_content_converter.content

    def test_should_get_content_when_none_raw_content_becomes_nonempty_raw_content(self):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.nonempty_content)

        assert self.nonempty_content == self.file_content_converter.content

    def test_should_get_content_when_nonempty_raw_content_becomes_empty_raw_content(self):
        self.file_content_converter.update(self.nonempty_content)
        self.file_content_converter.update("")

        assert self.nonempty_content == self.file_content_converter.content

    def test_should_get_empty_content_when_empty_raw_content_becomes_none_raw_content(self):
        self.file_content_converter.update("")
        self.file_content_converter.update(None)

        assert self.file_content_converter.content == {}

    def test_should_get_content_when_nonempty_raw_content_becomes_none_raw_content(self):
        self.file_content_converter.update(self.nonempty_content)
        self.file_content_converter.update(None)

        assert self.nonempty_content == self.file_content_converter.content

    def test_should_get_empty_content_when_empty_raw_content_becomes_xml_header_only_raw_content(
        self,
    ):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.xml_header_only_raw_content)

        assert self.file_content_converter.content == {}

    def test_should_get_content_when_empty_raw_content_becomes_xml_nonempty_raw_content(self):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        assert self.expected_xml_nonempty_content == self.file_content_converter.content

    def test_should_get_empty_content_when_given_xml_header_only_raw_content(self):
        self.file_content_converter.update(self.xml_header_only_raw_content)

        assert self.file_content_converter.content == {}

    def test_should_get_content_when_given_xml_nonempty_raw_content(self):
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        assert self.expected_xml_nonempty_content == self.file_content_converter.content

    def test_should_get_empty_content_when_none_raw_content_becomes_xml_header_only_raw_content(
        self,
    ):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.xml_header_only_raw_content)

        assert self.file_content_converter.content == {}

    def test_should_get_content_when_none_raw_content_becomes_xml_nonempty_raw_content(self):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        assert self.expected_xml_nonempty_content == self.file_content_converter.content

    def test_should_get_content_when_xml_header_only_raw_content_becomes_xml_nonempty_raw_content(
        self,
    ):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        assert self.expected_xml_nonempty_content == self.file_content_converter.content

    def test_should_get_content_when_xml_nonempty_raw_content_becomes_xml_header_only_raw_content(
        self,
    ):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update(self.xml_header_only_raw_content)

        assert self.file_content_converter.content == {}

    def test_should_get_content_when_xml_header_only_raw_content_becomes_empty_raw_content(self):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update("")

        assert self.file_content_converter.content == {}

    def test_should_get_content_when_xml_nonempty_raw_content_becomes_empty_raw_content(self):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update("")

        assert self.expected_xml_nonempty_content == self.file_content_converter.content

    def test_should_get_content_when_xml_header_only_raw_content_becomes_none_raw_content(self):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update(None)

        assert self.file_content_converter.content == {}

    def test_should_get_content_when_xml_nonempty_raw_content_becomes_none_raw_content(self):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update(None)

        assert self.expected_xml_nonempty_content == self.file_content_converter.content
