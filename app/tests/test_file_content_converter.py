import unittest
from unittest import mock
from time import sleep
import base64
import json

from app.src.file_content_converter import FileContentConverter

unavailable_content = {'url': "http://unavailable/content", 'content': None}
unavailable_to_empty_content = {'url': "http://unavailable_to_empty/content", 'counter': 0}
empty_content = {'url': "http://empty/content", 'content': {}}
empty_to_nonempty_content = {'url': "http://empty_to_non-empty/content", 'counter': 0}
nonempty_content = {'url': "http://non-empty/content",
                    'content': base64.b64encode(json.dumps({'test_key': "test_value"}).encode())}
nonempty_to_empty_content = {'url': "http://non-empty_to_empty/content", 'counter': 0}
nonempty_to_unavailable_content = {'url': "http://non-empty_to_unavailable/content", 'counter': 0}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == unavailable_content['url']:
        return MockResponse({'content': unavailable_content['content']}, 404)
    elif args[0] == unavailable_to_empty_content['url']:
        if unavailable_to_empty_content['counter'] == 0:
            unavailable_to_empty_content['counter'] += 1
            return MockResponse({'content': unavailable_content['content']}, 404)
        else:
            return MockResponse({'content': empty_content['content']}, 204)
    elif args[0] == empty_content['url']:
        return MockResponse({'content': empty_content['content']}, 204)
    elif args[0] == empty_to_nonempty_content['url']:
        if empty_to_nonempty_content['counter'] == 0:
            empty_to_nonempty_content['counter'] += 1
            return MockResponse({'content': empty_content['content']}, 204)
        else:
            return MockResponse({'content': nonempty_content['content']}, 200)
    elif args[0] == nonempty_content['url']:
        return MockResponse({'content': nonempty_content['content']}, 200)
    elif args[0] == nonempty_to_empty_content['url']:
        if nonempty_to_empty_content['counter'] == 0:
            nonempty_to_empty_content['counter'] += 1
            return MockResponse({'content': nonempty_content['content']}, 200)
        else:
            return MockResponse({'content': empty_content['content']}, 204)
    elif args[0] == nonempty_to_unavailable_content['url']:
        if nonempty_to_unavailable_content['counter'] == 0:
            nonempty_to_unavailable_content['counter'] += 1
            return MockResponse({'content': nonempty_content['content']}, 200)
        else:
            return MockResponse({}, 404)
    else:
        return MockResponse(None, 404)


@mock.patch('app.src.file_content_converter.requests.get', side_effect=mocked_requests_get)
class TestFileContentConverter(unittest.TestCase):
    def setUp(self):
        self.set_test_arguments()
        self.set_tested_objects()
        self.set_test_expected_results()

    def set_test_arguments(self):
        pass

    def set_tested_objects(self):
        pass

    def set_test_expected_results(self):
        pass

    def test_Should_GetEmptyDict_When_RawContentIsNotAvailable(self, mock_get):
        self.file_content_converter = FileContentConverter(unavailable_content['url'])

        wait_monitoring_interval_time_with_buffer()

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetEmptyDict_When_NotAvailableRawContentBecomesAvailableAndIsEmptyDict(self, mock_get):
        self.file_content_converter = FileContentConverter(unavailable_to_empty_content['url'])

        wait_monitoring_interval_time_with_buffer()

        self.assertEqual({}, self.file_content_converter.content)

    def test_Should_GetEmptyDict_When_RawContentIsEmptyDict(self, mock_get):
        self.file_content_converter = FileContentConverter(empty_content['url'])

        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(empty_content['content'], self.file_content_converter.content)

    def test_Should_GetDictContent_When_EmptyDictRawContentIsUpdated(self, mock_get):
        self.file_content_converter = FileContentConverter(empty_to_nonempty_content['url'])

        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(base64.b64decode(nonempty_content['content']).decode(), self.file_content_converter.content)

    def test_Should_GetDictContent_When_RawContentIsNotEmptyDict(self, mock_get):
        self.file_content_converter = FileContentConverter(nonempty_content['url'])

        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(base64.b64decode(nonempty_content['content']).decode(), self.file_content_converter.content)

    def test_Should_GetEmptyDict_When_RawContentBecomesEmptyDict(self, mock_get):
        self.file_content_converter = FileContentConverter(nonempty_to_empty_content['url'])

        wait_monitoring_interval_time_with_buffer()

        self.assertEqual(empty_content['content'], self.file_content_converter.content)

    def test_Should_GetEmptyDict_When_RawContentBecomesNotAvailable(self, mock_get):
        self.file_content_converter = FileContentConverter(nonempty_to_unavailable_content['url'])

        wait_monitoring_interval_time_with_buffer()

        self.assertEqual({}, self.file_content_converter.content)


def wait_monitoring_interval_time_with_buffer():
    monitoring_interval_time = 5
    buffer = 1
    sleep(monitoring_interval_time + buffer)
