import unittest
from pathlib import Path
from unittest import mock

from src.file_content_converter import FileContentConverter

url = "http://subscriber/update"


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == url:
        return MockResponse(None, 204)
    else:
        return MockResponse(None, 404)


@mock.patch("src.file_content_converter.requests.post", side_effect=mocked_requests_post)
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

        self.file_content_converter = FileContentConverter(url)

    def test_Should_GetEmptyContent_When_GivenNoneRawContent(self, mock_get):
        self.file_content_converter.update(None)

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetEmptyContent_When_NoneRawContentBecomesEmptyRawContent(self, mock_get):
        self.file_content_converter.update(None)
        self.file_content_converter.update("")

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetEmptyContent_When_GivenEmptyRawContent(self, mock_get):
        self.file_content_converter.update("")

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_EmptyRawContentBecomesNonemptyRawContent(self, mock_get):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)
        self.assertEqual(204, self.file_content_converter.response.status_code)
        self.assertEqual(None, self.file_content_converter.response.json())

    def test_Should_GetContent_When_GivenNonemptyRawContent(self, mock_get):
        self.file_content_converter.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)
        self.assertEqual(204, self.file_content_converter.response.status_code)
        self.assertEqual(None, self.file_content_converter.response.json())

    def test_Should_GetContent_When_NoneRawContentBecomesNonemptyRawContent(self, mock_get):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.nonempty_content)

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)
        self.assertEqual(204, self.file_content_converter.response.status_code)
        self.assertEqual(None, self.file_content_converter.response.json())

    def test_Should_GetContent_When_NonemptyRawContentBecomesEmptyRawContent(self, mock_get):
        self.file_content_converter.update(self.nonempty_content)
        self.file_content_converter.update("")

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetEmptyContent_When_EmptyRawContentBecomesNoneRawContent(self, mock_get):
        self.file_content_converter.update("")
        self.file_content_converter.update(None)

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_NonemptyRawContentBecomesNoneRawContent(self, mock_get):
        self.file_content_converter.update(self.nonempty_content)
        self.file_content_converter.update(None)

        self.assertEqual(self.nonempty_content, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetEmptyContent_When_EmptyRawContentBecomesXMLHeaderOnlyRawContent(self, mock_get):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_EmptyRawContentBecomesXMLNonemptyRawContent(self, mock_get):
        self.file_content_converter.update("")
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)
        self.assertEqual(204, self.file_content_converter.response.status_code)
        self.assertEqual(None, self.file_content_converter.response.json())

    def test_Should_GetEmptyContent_When_GivenXMLHeaderOnlyRawContent(self, mock_get):
        self.file_content_converter.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_GivenXMLNonemptyRawContent(self, mock_get):
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)
        self.assertEqual(204, self.file_content_converter.response.status_code)
        self.assertEqual(None, self.file_content_converter.response.json())

    def test_Should_GetEmptyContent_When_NoneRawContentBecomesXMLHeaderOnlyRawContent(self, mock_get):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_NoneRawContentBecomesXMLNonemptyRawContent(self, mock_get):
        self.file_content_converter.update(None)
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)
        self.assertEqual(204, self.file_content_converter.response.status_code)
        self.assertEqual(None, self.file_content_converter.response.json())

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesXMLNonemptyRawContent(self, mock_get):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update(self.xml_nonempty_raw_content)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)
        self.assertEqual(204, self.file_content_converter.response.status_code)
        self.assertEqual(None, self.file_content_converter.response.json())

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesXMLHeaderOnlyRawContent(self, mock_get):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update(self.xml_header_only_raw_content)

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesEmptyRawContent(self, mock_get):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update("")

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesEmptyRawContent(self, mock_get):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update("")

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_XMLHeaderOnlyRawContentBecomesNoneRawContent(self, mock_get):
        self.file_content_converter.update(self.xml_header_only_raw_content)
        self.file_content_converter.update(None)

        self.assertEqual({}, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)

    def test_Should_GetContent_When_XMLNonemptyRawContentBecomesNoneRawContent(self, mock_get):
        self.file_content_converter.update(self.xml_nonempty_raw_content)
        self.file_content_converter.update(None)

        self.assertEqual(self.expected_xml_nonempty_content, self.file_content_converter.content)
        self.assertEqual(None, self.file_content_converter.response)
