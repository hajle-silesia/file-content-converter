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
        with open(pathlib.Path(__file__).parent / "./files/converter.xml", encoding="utf-8") as file:
            cls.xml_nonempty_raw_content = file.read()

        cls.producer = MockProducer()

        cls.expected_xml_nonempty_content = {'note': {'to': "Smith",
                                                      'from': "Adams",
                                                      'heading': "Test",
                                                      'body': "Test body",
                                                      },
                                             }

    def setUp(self):
        super().setUp()

        self.file_content_converter = FileContentConverter(self.producer)

    def test_Should_GetEmptyContent_When_GivenNoneRawContent(self):
        self.file_content_converter.update(None)

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetEmptyContent_When_NoneRawContentBecomesEmptyRawContent(self):
        self.file_content_converter.update(None)
        self.file_content_converter.update("")

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetEmptyContent_When_GivenEmptyRawContent(self):
        self.file_content_converter.update("")

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetContent_When_EmptyRawContentBecomesNonemptyRawContent(self):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)

    def test_Should_GetContent_When_GivenNonemptyRawContent(self):
        self.file_content_converter.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)

    def test_Should_GetContent_When_NoneRawContentBecomesNonemptyRawContent(self):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)

    def test_Should_GetContent_When_NonemptyRawContentBecomesEmptyRawContent(self):
        self.file_content_converter.update(self.nonempty_content)
        self.file_content_converter.update("")

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)

    def test_Should_GetEmptyContent_When_EmptyRawContentBecomesNoneRawContent(self):
        self.file_content_converter.update("")
        self.file_content_converter.update(None)

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetContent_When_NonemptyRawContentBecomesNoneRawContent(self):
        self.file_content_converter.update(self.nonempty_content)
        self.file_content_converter.update(None)

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)

    def test_Should_GetEmptyContent_When_EmptyRawContentBecomesXMLHeaderOnlyRawContent(self):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetContent_When_EmptyRawContentBecomesXMLNonemptyRawContent(self):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)

    def test_Should_GetEmptyContent_When_GivenXMLHeaderOnlyRawContent(self):
        self.file_content_converter.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetContent_When_GivenXMLNonemptyRawContent(self):
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)

    def test_Should_GetEmptyContent_When_NoneRawContentBecomesXMLHeaderOnlyRawContent(self):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetContent_When_NoneRawContentBecomesXMLNonemptyRawContent(self):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesXMLNonemptyRawContent(self):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesXMLHeaderOnlyRawContent(self):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesEmptyRawContent(self):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update("")

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesEmptyRawContent(self):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update("")

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesNoneRawContent(self):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update(None)

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesNoneRawContent(self):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update(None)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)
