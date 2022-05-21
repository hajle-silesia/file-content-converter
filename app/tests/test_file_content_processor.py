import base64
import unittest
from pathlib import Path
from time import sleep
from unittest import mock

from app.src.file_content_processor import FileContentProcessor

with open(Path(__file__).parent / "./files/converter.xml", encoding="utf-8") as file:
    xml_content = file.read()

empty_response = {'url': "http://empty/content", 'content': ""}
header_only_response = {'url': "http://header-only/content", 'content': "<?xml version='1.0' encoding='UTF-8'?>"}
nonempty_response = {'url': "http://nonempty/content", 'content': xml_content}

responses = [empty_response,
             header_only_response,
             nonempty_response,
             ]
for response in responses:
    response['content_encoded'] = base64.b64encode(response['content'].encode())


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == empty_response['url']:
        return MockResponse({'content': empty_response['content_encoded']}, 204)
    elif args[0] == header_only_response['url']:
        return MockResponse({'content': header_only_response['content_encoded']}, 204)
    elif args[0] == nonempty_response['url']:
        return MockResponse({'content': nonempty_response['content_encoded']}, 200)
    else:
        return MockResponse(None, 404)


@mock.patch('app.src.file_content_processor.requests.get', side_effect=mocked_requests_get)
class TestFileContentConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_expected_results()

    @classmethod
    def set_test_arguments(cls):
        pass

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_expected_results(cls):
        cls.expected_empty_content = {}
        cls.expected_nonempty_content = {'note': {'to': "Smith",
                                                  'from': "Adams",
                                                  'heading': "Test",
                                                  'body': "Test body",
                                                  },
                                         }

    def test_Should_GetEmptyContent_When_GivenEmptyRawContent(self, mock_get):
        self.file_content_processor = FileContentProcessor(empty_response['url'])
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_empty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenHeaderOnlyContent(self, mock_get):
        self.file_content_processor = FileContentProcessor(header_only_response['url'])
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_empty_content, self.file_content_processor.content)

    def test_Should_GetNonemptyContent_When_GivenNonemptyRawContent(self, mock_get):
        self.file_content_processor = FileContentProcessor(nonempty_response['url'])
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_nonempty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenEmptyRawContentBecomesHeaderOnly(self, mock_get):
        self.file_content_processor = FileContentProcessor(empty_response['url'])
        wait_monitoring_interval_time_with_buffer()
        self.file_content_processor.url = header_only_response['url']
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_empty_content, self.file_content_processor.content)

    def test_Should_GetNonemptyContent_When_GivenHeaderOnlyRawContentBecomesNonempty(self, mock_get):
        self.file_content_processor = FileContentProcessor(header_only_response['url'])
        wait_monitoring_interval_time_with_buffer()
        self.file_content_processor.url = nonempty_response['url']
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_nonempty_content, self.file_content_processor.content)

    def test_Should_GetNonemptyContent_When_GivenEmptyRawContentBecomesNonempty(self, mock_get):
        self.file_content_processor = FileContentProcessor(empty_response['url'])
        wait_monitoring_interval_time_with_buffer()
        self.file_content_processor.url = nonempty_response['url']
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_nonempty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenNonemptyRawContentBecomesHeaderOnly(self, mock_get):
        self.file_content_processor = FileContentProcessor(nonempty_response['url'])
        wait_monitoring_interval_time_with_buffer()
        self.file_content_processor.url = header_only_response['url']
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_empty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenHeaderOnlyRawContentBecomesEmpty(self, mock_get):
        self.file_content_processor = FileContentProcessor(header_only_response['url'])
        wait_monitoring_interval_time_with_buffer()
        self.file_content_processor.url = empty_response['url']
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_empty_content, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenNonemptyRawContentBecomesEmpty(self, mock_get):
        self.file_content_processor = FileContentProcessor(nonempty_response['url'])
        wait_monitoring_interval_time_with_buffer()
        self.file_content_processor.url = empty_response['url']
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.expected_empty_content, self.file_content_processor.content)


def wait_monitoring_interval_time_with_buffer():
    monitoring_interval_time = 5
    buffer = 1
    sleep(monitoring_interval_time + buffer)
