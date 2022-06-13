import unittest
from pathlib import Path

from src.file_content_converter import FileContentConverter

url = "http://subscriber/update"


class TestFileContentConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_expected_results()

    @classmethod
    def set_test_arguments(cls):
        cls.nonempty_content = "test_content"

        cls.xml_header_only_raw_content = "<?xml version='1.0' encoding='UTF-8'?>"
        with open(Path(__file__).parent / "./files/converter.xml", encoding="utf-8") as file:
            cls.xml_nonempty_raw_content = file.read()

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_expected_results(cls):
        cls.expected_xml_nonempty_content = {'note': {'to': "Smith",
                                                      'from': "Adams",
                                                      'heading': "Test",
                                                      'body': "Test body",
                                                      },
                                             }

    def setUp(self):
        super().setUp()

        self.file_content_processor = FileContentConverter(url)

    def test_Should_GetEmptyContent_When_GivenNoneRawContent(self):
        self.file_content_processor.update(None)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_NoneRawContentBecomesEmptyRawContent(self):
        self.file_content_processor.update(None)
        self.file_content_processor.update("")

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenEmptyRawContent(self):
        self.file_content_processor.update("")

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_EmptyRawContentBecomesNonemptyRawContent(self):
        self.file_content_processor.update("")
        self.file_content_processor.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_processor.content)

    def test_Should_GetContent_When_GivenNonemptyRawContent(self):
        self.file_content_processor.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_processor.content)

    def test_Should_GetContent_When_NoneRawContentBecomesNonemptyRawContent(self):
        self.file_content_processor.update(None)
        self.file_content_processor.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_processor.content)

    def test_Should_GetContent_When_NonemptyRawContentBecomesEmptyRawContent(self):
        self.file_content_processor.update(self.nonempty_content)
        self.file_content_processor.update("")

        self.assertEqual(self.nonempty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_EmptyRawContentBecomesNoneRawContent(self):
        self.file_content_processor.update("")
        self.file_content_processor.update(None)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_NonemptyRawContentBecomesNoneRawContent(self):
        self.file_content_processor.update(self.nonempty_content)
        self.file_content_processor.update(None)

        self.assertEqual(self.nonempty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_EmptyRawContentBecomesXMLHeaderOnlyRawContent(self):
        self.file_content_processor.update("")
        self.file_content_processor.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_EmptyRawContentBecomesXMLNonemptyRawContent(self):
        self.file_content_processor.update("")
        self.file_content_processor.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenXMLHeaderOnlyRawContent(self):
        self.file_content_processor.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_GivenXMLNonemptyRawContent(self):
        self.file_content_processor.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_NoneRawContentBecomesXMLHeaderOnlyRawContent(self):
        self.file_content_processor.update(None)
        self.file_content_processor.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_NoneRawContentBecomesXMLNonemptyRawContent(self):
        self.file_content_processor.update(None)
        self.file_content_processor.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_processor.content)

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesXMLNonemptyRawContent(self):
        self.file_content_processor.update(self.xml_header_only_raw_content)
        self.file_content_processor.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_processor.content)

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesXMLHeaderOnlyRawContent(self):
        self.file_content_processor.update(self.xml_nonempty_raw_content)
        self.file_content_processor.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesEmptyRawContent(self):
        self.file_content_processor.update(self.xml_header_only_raw_content)
        self.file_content_processor.update("")

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesEmptyRawContent(self):
        self.file_content_processor.update(self.xml_nonempty_raw_content)
        self.file_content_processor.update("")

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_processor.content)

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesNoneRawContent(self):
        self.file_content_processor.update(self.xml_header_only_raw_content)
        self.file_content_processor.update(None)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesNoneRawContent(self):
        self.file_content_processor.update(self.xml_nonempty_raw_content)
        self.file_content_processor.update(None)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_processor.content)
